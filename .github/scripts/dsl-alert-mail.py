#!/usr/bin/env python3
"""dsl-alert-mail.py [--html] [--to A,B] [--cc C,D] <subject> [body] - mail through Graph.

VENDORED COPY. The canonical version lives in `hertie-data-science-lab/ds01-infra` at
`scripts/maintenance/dsl-alert-mail.py`; change it there first and copy the result here,
so the box and this repo never send through two different scripts.

The mail channel of `dsl-alert.sh`. Teams is a webhook this box may or may not have;
this is the channel that reaches a human who is not looking at the journal.

One transport, Microsoft Graph (application auth, certificate credential). There is
deliberately no SMTP fallback: the tenant disables SMTP AUTH, so a fallback could never
fire, and an alerter with a second untested send path is an alerter that fails silently.

Configured entirely from the environment, so the credential lives in one root-only file
(`/etc/dsl-alert-mail.env`, EnvironmentFile of `dsl-alert@.service`) and never in the repo:

    GRAPH_TENANT_ID        the Entra tenant
    GRAPH_CLIENT_ID        the lab's app registration
    GRAPH_SENDER           mailbox to send as, e.g. datasciencelab@hertie-school.org
    DSL_ALERT_TO           where the alert goes - one address or a comma-separated list
    DSL_ALERT_CC           optional, copied on every alert - same comma-separated form

and exactly one of, holding the certificate then its unencrypted private key:

    GRAPH_CLIENT_CERT_FILE a path, for a host that keeps the PEM in a root-only file
    GRAPH_CLIENT_CERT      the PEM itself, for GitHub Actions, where a secret is a value
                           and not a file. Same content as the toolkit's secret of that
                           name. Setting both is refused rather than silently preferring
                           one: two credentials in one environment is a rotation that went
                           half-finished, and picking a winner hides it.

Any of those still unset when the mailer runs is read out of `/etc/dsl-alert-mail.env`
itself (override with DSL_ALERT_ENV_FILE), because systemd is not the only caller: the
config watchdog and the monthly report run from cron, which inherits no EnvironmentFile.
The environment always wins over the file, and the file is parsed, never sourced - see
`load_env_file`.

`--to` REPLACES the environment for one call. `--cc` ADDS to it, and the asymmetry is the
point: DSL_ALERT_CC is the archive mailbox, which is copied on everything this lab sends,
and a caller that names a further recipient - a ticket notifier copying whoever opened the
ticket - must not be able to drop the archive by doing so. Nothing here can turn the
archive off; unsetting the variable is the only way, and that is a deployment decision.

An address on the Cc line that does not parse is DROPPED, with a masked line saying so; a
To address that does not parse is fatal. The difference is who typed it: the To line is
ours, and the Cc may carry whatever a public web form collected. Graph rejects the whole
message for one malformed recipient, so an un-vetted Cc would cost the alert itself.

The credential is a certificate, not a secret: the token request sends a thumbprint that
identifies the certificate and a signature made by the matching key, both derived from the
one PEM, so the two halves cannot drift apart. Entra never sees the private key.

Provisioning steps are in docs/admin/maintenance.md. Body on stdin, not argv: `/proc` on
this box is world-readable, so anything on a command line is visible in `ps`.

Prints status codes and one-line outcomes only. Never a token, and never a response body -
a Graph error body echoes the request back, recipient included.
"""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

_AUTHORITY = "https://login.microsoftonline.com"
_GRAPH = "https://graph.microsoft.com/v1.0"
_SCOPE = "https://graph.microsoft.com/.default"
_ASSERTION_TYPE = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
# The assertion is single-use and consumed immediately; a short life caps the replay window.
_ASSERTION_TTL = 300

MAIL_ENV = (
    "GRAPH_TENANT_ID",
    "GRAPH_CLIENT_ID",
    "GRAPH_SENDER",
)
# Resolved separately from MAIL_ENV, because `--to` replaces this rather than adding to it:
# requiring the variable a flag exists to override is how a caller ends up setting a dummy.
TO_ENV = "DSL_ALERT_TO"
# The two ways the certificate can arrive. Exactly one, never both - see the docstring.
CERT_ENV = ("GRAPH_CLIENT_CERT_FILE", "GRAPH_CLIENT_CERT")
# Optional: a standing Cc, for a caller that always copies the same archive mailbox.
CC_ENV = "DSL_ALERT_CC"
# The box keeps the mail credential in this file, and `dsl-alert@.service` hands it over as
# an EnvironmentFile. A CRON job inherits nothing from systemd, and two of this mailer's
# callers - config-watchdog.sh and ds01-monthly-report - run from cron, so without this
# they would be configured under systemd and unconfigured on a schedule. Read here, once,
# rather than in each caller: one parser, and a new caller is configured by existing.
ENV_FILE_ENV = "DSL_ALERT_ENV_FILE"
DEFAULT_ENV_FILE = "/etc/dsl-alert-mail.env"
# Every one of these is interpolated into a URL or a header. The address lists are checked
# per address instead, after the split - a comma-separated list is whitespace-legal.
_SINGLE_LINE = ("GRAPH_TENANT_ID", "GRAPH_CLIENT_ID", "GRAPH_SENDER")

# Deliberately not RFC 5322. This rejects the shapes a hand-typed form field actually
# produces - a bare username, a trailing comma, an address with a space in it - and lets
# everything else through to Graph, which is the real authority on what it will accept.
_ADDRESS_RE = re.compile(r"^[^@\s,<>]+@[^@\s,<>]+\.[^@\s,<>]+$")

# Graph answers a throttled or briefly-unhealthy request with one of these and, on a 429,
# a Retry-After. One retry only: this is an alert about an outage, not a mail merge, and a
# second failure is itself worth reporting.
_RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
_MAX_SEND_ATTEMPTS = 2
_RETRY_AFTER_DEFAULT = 5.0  # when the header is absent or unreadable
_RETRY_AFTER_CAP = 60.0  # a header we cannot vet must not park the unit
_TIMEOUT = 20


@dataclass
class Config:
    tenant_id: str
    client_id: str
    sender: str
    cert_pem: bytes
    to: tuple[str, ...]
    cc: tuple[str, ...] = ()


def log(msg: str) -> None:
    print(msg, flush=True)


def mask_email(addr: str) -> str:
    """`a***@domain` - enough to tell two recipients apart in the journal, not enough to
    identify either. The journal of a failed unit is posted to Teams."""
    local, _, domain = addr.partition("@")
    return f"{local[:1]}***@{domain}" if domain else f"{local[:1]}***"


def split_addresses(raw: str) -> tuple[str, ...]:
    """A comma-separated address list as a tuple, blanks and stray whitespace dropped."""
    return tuple(part.strip() for part in raw.split(",") if part.strip())


def vet_addresses(addresses: tuple[str, ...], line: str, *, fatal: bool) -> tuple[str, ...]:
    """The addresses that parse, or () if a `fatal` line held even one that did not.

    The two lines are vetted differently because different people typed them. The To line
    is ours, from a config file we control, so a bad address there is a misconfiguration
    and sending to the rest would quietly deliver less than was asked for. The Cc line can
    carry whatever a public web form collected, and Graph rejects the WHOLE message for one
    malformed recipient - so a bad Cc is dropped and the alert still goes.

    Masked in the log either way: this runs in GitHub Actions on a PUBLIC repo as well as
    on the box."""
    bad = [a for a in addresses if not _ADDRESS_RE.match(a)]
    for addr in bad:
        log(f"{line}: {'unusable' if fatal else 'dropped'} address {mask_email(addr)}")
    if bad and fatal:
        return ()
    return tuple(a for a in addresses if _ADDRESS_RE.match(a))


def resolve_cert() -> bytes | None:
    """The certificate PEM, from a file or straight out of the environment.

    Exactly one of CERT_ENV, because two is a half-finished rotation (see the docstring)
    and none is a missing credential. Returns the PEM bytes so everything downstream is
    identical whichever way it arrived."""
    present = [k for k in CERT_ENV if (os.environ.get(k) or "").strip()]
    if len(present) != 1:
        which = " and ".join(present) if present else "neither"
        log(f"mail alert not configured - set exactly one of {', '.join(CERT_ENV)} ({which} set)")
        return None
    name = present[0]
    value = (os.environ[name] or "").strip()
    if name == "GRAPH_CLIENT_CERT":
        return value.encode()
    try:
        return Path(value).read_bytes()
    except OSError as exc:
        log(f"GRAPH_CLIENT_CERT_FILE unreadable: {exc}")
        return None


def _masked(addresses: tuple[str, ...]) -> str:
    """A message's recipients, masked - `a***@x.org, b***@x.org`."""
    return ", ".join(mask_email(a) for a in addresses)


def _cc_note(cfg: Config) -> str:
    """The Cc line for a log message, or nothing when there is no Cc."""
    return f" cc {_masked(cfg.cc)}" if cfg.cc else ""


def load_env_file() -> None:
    """Fill in the mail variables from `/etc/dsl-alert-mail.env` for a caller systemd did
    not start - a cron job, or a hand-run report.

    The environment always WINS: `dsl-alert@.service` already passes this file as an
    EnvironmentFile, Actions passes secrets, and a one-off `DSL_ALERT_TO=... ` on the front
    of a command has to keep meaning what it says. So this only fills gaps.

    Only the variables this script knows about are read out of the file. It is a root-only
    file, so a hostile line is not the threat - a stray `PATH=` or `LD_PRELOAD=` left in it
    by an admin is, and a mailer that quietly rewrote its own PATH would be very hard to
    explain. For the same reason the file is PARSED and never sourced.

    Absent or unreadable is a silent no-op: on a box with no mail provisioning, and in
    Actions, there is no such file and nothing is wrong with that. `config_from_env` still
    reports what is missing, by name.

    `KEY=value`, one per line, `#` comments, an optional `export ` prefix and one layer of
    surrounding quotes - the subset systemd's own EnvironmentFile accepts, which is what
    the provisioning recipe in docs/admin/maintenance.md writes. A multi-line value is not
    supported, which is why the box uses GRAPH_CLIENT_CERT_FILE and not GRAPH_CLIENT_CERT.
    """
    path = Path(os.environ.get(ENV_FILE_ENV) or DEFAULT_ENV_FILE)
    try:
        text = path.read_text()
    except OSError:
        return
    wanted = {*MAIL_ENV, *CERT_ENV, TO_ENV, CC_ENV}
    for raw in text.splitlines():
        line = raw.strip().removeprefix("export ")
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or key not in wanted or (os.environ.get(key) or "").strip():
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ[key] = value


def config_from_env(to: str | None = None, cc: str | None = None) -> Config | None:
    """Build the config from the environment, or None if it is unusable.

    `to` REPLACES DSL_ALERT_TO for this call; `cc` is ADDED to DSL_ALERT_CC rather than
    replacing it, so a caller naming one more recipient cannot drop the archive mailbox.
    See the module docstring.

    Names the variables at fault rather than saying "not configured": the values are a
    root-only file nobody can read back from a journal line, so a blanket message is
    undebuggable. A partly-filled env is a misconfiguration, not an absence."""
    load_env_file()
    found = {k: (os.environ.get(k) or "").strip() for k in MAIL_ENV}
    missing = [k for k, v in found.items() if not v]
    if missing:
        log(f"mail alert not configured - unset or blank: {', '.join(missing)}")
        return None
    ragged = [k for k in _SINGLE_LINE if any(c.isspace() for c in found[k])]
    if ragged:
        log(f"mail alert misconfigured - whitespace inside {', '.join(ragged)}")
        return None
    cert_pem = resolve_cert()
    if cert_pem is None:
        return None
    raw_to = to if to is not None else (os.environ.get(TO_ENV) or "")
    to_line = "--to" if to is not None else TO_ENV
    recipients = vet_addresses(split_addresses(raw_to), to_line, fatal=True)
    if not recipients:
        log(f"mail alert not configured - {to_line} carried no usable address")
        return None
    # Standing archive Cc first, then whatever this call added - vetted under the name of
    # whichever supplied it, so a rejected address points at the thing to go and fix.
    copies = vet_addresses(
        split_addresses(os.environ.get(CC_ENV) or ""), CC_ENV, fatal=False
    ) + vet_addresses(split_addresses(cc or ""), "--cc", fatal=False)
    # A recipient named twice - on both Cc sources, or on Cc and To - gets one copy.
    seen = {a.lower() for a in recipients}
    deduped = []
    for addr in copies:
        if addr.lower() not in seen:
            seen.add(addr.lower())
            deduped.append(addr)
    copies = tuple(deduped)
    return Config(
        tenant_id=found["GRAPH_TENANT_ID"],
        client_id=found["GRAPH_CLIENT_ID"],
        sender=found["GRAPH_SENDER"],
        cert_pem=cert_pem,
        to=recipients,
        cc=copies,
    )


def _b64url(raw: bytes) -> str:
    """Unpadded base64url - what JWS uses for every segment."""
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _load_cert_and_key(raw: bytes) -> tuple[x509.Certificate, rsa.RSAPrivateKey]:
    """Parse the PEM into (certificate, private key).

    Takes the bytes rather than a path, because the same PEM arrives as a file on the box
    and as a secret VALUE in Actions - `resolve_cert` has already made those one thing.

    Raises RuntimeError, not the library's own errors: a malformed credential should read
    as one actionable journal line, not a cryptography traceback out of an alerter."""
    try:
        cert = x509.load_pem_x509_certificate(raw)
    except ValueError as exc:
        raise RuntimeError(
            f"the credential has no readable PEM certificate ({exc}). It must hold the "
            f"certificate AND its private key, as `cat cert.cer key.pem` produces."
        ) from exc
    try:
        key = serialization.load_pem_private_key(raw, password=None)
    except (ValueError, TypeError) as exc:
        # TypeError is what cryptography raises for an ENCRYPTED key given no password -
        # a passphrase can never work here, since no one can type one into a systemd unit
        # or a workflow step.
        raise RuntimeError(
            f"the credential has no usable PEM private key ({exc}). The key must be in "
            f"the same PEM and must not be passphrase-protected."
        ) from exc
    if not isinstance(key, rsa.RSAPrivateKey):
        raise RuntimeError(  # noqa: TRY004
            f"the credential holds a {type(key).__name__} private key; Entra app "
            f"certificate credentials must be RSA."
        )
    return cert, key


def _client_assertion(cfg: Config) -> str:
    """A JWT signed by the app's private key, standing in for a client secret.

    Entra looks the public half up by the `x5t` thumbprint in the header, then checks the
    signature against it. `x5t` is SHA-1 because the protocol says so - it is a certificate
    IDENTIFIER, not a security control; the signature itself is RS256 (SHA-256)."""
    cert, key = _load_cert_and_key(cfg.cert_pem)
    now = int(time.time())
    header = {
        "alg": "RS256",
        "typ": "JWT",
        "x5t": _b64url(cert.fingerprint(hashes.SHA1())),  # identifier only, see docstring
    }
    claims = {
        "aud": f"{_AUTHORITY}/{cfg.tenant_id}/oauth2/v2.0/token",
        "iss": cfg.client_id,
        "sub": cfg.client_id,
        "jti": str(uuid.uuid4()),
        "nbf": now,
        "exp": now + _ASSERTION_TTL,
    }
    signing_input = ".".join(
        _b64url(json.dumps(part, separators=(",", ":")).encode()) for part in (header, claims)
    )
    signature = key.sign(signing_input.encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{signing_input}.{_b64url(signature)}"


def _response_headers(raw) -> dict[str, str]:
    """A response's headers as a lower-cased dict (HTTP header names are case-insensitive,
    and `Retry-After` arrives spelled however the server felt like spelling it)."""
    try:
        return {k.lower(): v for k, v in raw.items()}
    except AttributeError:
        return {}


def _post(url: str, data: bytes, headers: dict[str, str]) -> tuple[int, bytes, dict]:
    """POST and return (status, body, response headers); network and HTTP errors come back
    as a status, so no caller has to handle an exception to see a failure."""
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return resp.status, resp.read(), _response_headers(resp.headers)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), _response_headers(exc.headers)
    except urllib.error.URLError as exc:
        return 0, str(exc.reason).encode(), {}
    except (http.client.HTTPException, ValueError, TimeoutError) as exc:
        return 0, str(exc).encode(), {}


def retry_after_seconds(headers: dict[str, str]) -> float:
    """How long `Retry-After` asks us to wait, in seconds - capped, and defaulted when the
    header is missing or is the HTTP-date form we do not parse."""
    raw = (headers.get("retry-after") or "").strip()
    try:
        wait = float(raw)
    except ValueError:
        return _RETRY_AFTER_DEFAULT
    return min(max(wait, 0.0), _RETRY_AFTER_CAP)


def graph_token(cfg: Config) -> str | None:
    """A client-credentials access token for Graph, or None on failure."""
    url = f"{_AUTHORITY}/{cfg.tenant_id}/oauth2/v2.0/token"
    body = urllib.parse.urlencode(
        {
            "client_id": cfg.client_id,
            "client_assertion_type": _ASSERTION_TYPE,
            "client_assertion": _client_assertion(cfg),
            "scope": _SCOPE,
            "grant_type": "client_credentials",
        }
    ).encode()
    status, raw, _headers = _post(url, body, {"Content-Type": "application/x-www-form-urlencoded"})
    if status != 200:
        # Status only: an Entra error body quotes the assertion back.
        log(f"Graph token request failed ({status})")
        return None
    try:
        token = json.loads(raw).get("access_token")
    except ValueError:
        token = None
    if not token:
        log("Graph token response carried no access_token")
        return None
    return token


def send_mail(cfg: Config, token: str, subject: str, body: str, *, html: bool = False) -> bool:
    """Send one message as `sender`, to everyone on `cfg.to`, copying `cfg.cc`.

    One POST however many recipients: the text is identical for all of them, and a
    per-recipient loop would pay the rate limiter's send slot for each identical copy.

    `html` sends `contentType: HTML`. The monthly report needs it - its heatmap and bar
    chart are ASCII, and only a `<pre>` keeps them aligned in a mail client that would
    otherwise reflow them into noise."""
    url = f"{_GRAPH}/users/{urllib.parse.quote(cfg.sender)}/sendMail"
    message: dict = {
        "subject": subject,
        "body": {"contentType": "HTML" if html else "Text", "content": body},
        "toRecipients": [{"emailAddress": {"address": a}} for a in cfg.to],
    }
    if cfg.cc:
        message["ccRecipients"] = [{"emailAddress": {"address": a}} for a in cfg.cc]
    payload = json.dumps(
        {
            "message": message,
            # Nothing reads the shared mailbox's Sent Items, and an outage can mean one
            # alert per tick. A caller that wants the mailbox to KEEP a copy - the ticket
            # notifier, the monthly report - puts the mailbox on the Cc line instead.
            "saveToSentItems": False,
        }
    ).encode()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    for attempt in range(1, _MAX_SEND_ATTEMPTS + 1):
        status, _raw, response_headers = _post(url, payload, headers)
        if status in (200, 202):
            log(f"alert mailed to {_masked(cfg.to)}{_cc_note(cfg)} ({status})")
            return True
        if status in _RETRY_STATUSES and attempt < _MAX_SEND_ATTEMPTS:
            # A throttle or a brief 5xx is Graph asking to be asked again, not a bad
            # recipient. One more try, then report it.
            wait = retry_after_seconds(response_headers)
            log(f"send got {status}, retrying once in {wait:g}s")
            time.sleep(wait)
            continue
        # Status only: a Graph error body echoes the message, recipient included.
        log(f"send to {_masked(cfg.to)} failed ({status})")
        return False
    return False


class _Parser(argparse.ArgumentParser):
    """An ArgumentParser that reports a bad command line the way this script reports
    everything else: one line on stdout, exit 1.

    argparse's own behaviour is a usage block on stderr and exit 2. This runs under systemd
    and under Actions, where stdout is the journal and the run log - splitting the one
    message a caller gets across two streams, and returning a code the rest of the script
    never uses, would make a typo in a unit file read as a different failure from every
    other failure here."""

    def error(self, message: str) -> None:  # type: ignore[override]
        raise _Usage(message)


class _Usage(Exception):
    """A bad command line, carrying argparse's own complaint."""


def main(argv: list[str]) -> int:
    parser = _Parser(
        prog="dsl-alert-mail.py",
        description="Mail one alert through Microsoft Graph.",
        add_help=False,
    )
    parser.add_argument("--html", action="store_true", help="send the body as HTML")
    parser.add_argument("--to", help=f"comma-separated, overrides {TO_ENV}")
    parser.add_argument("--cc", help=f"comma-separated, added to {CC_ENV}")
    parser.add_argument("subject")
    # Body on stdin by default, not argv: /proc on the box is world-readable, so a journal
    # tail on a command line is a journal tail in `ps`.
    parser.add_argument("body", nargs="?", help="read from stdin when omitted")
    try:
        args = parser.parse_args(argv)
    except _Usage as exc:
        log(f"usage: {parser.format_usage().strip()} - {exc}")
        return 1

    body = args.body if args.body is not None else sys.stdin.read()

    cfg = config_from_env(to=args.to, cc=args.cc)
    if cfg is None:
        return 1
    try:
        token = graph_token(cfg)
    except RuntimeError as exc:
        log(f"mail alert failed: {exc}")
        return 1
    if token is None:
        return 1
    return 0 if send_mail(cfg, token, args.subject, body, html=args.html) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
