#!/usr/bin/env python3
"""notify_ticket.py - mail a newly opened ds01-hub ticket to the lab, then redact it.

Run by `.github/workflows/notify-ticket.yml` on `issues: [opened]`. Before this existed a
filed ticket notified nobody: the assignee was a login the repo cannot assign (GitHub drops
those silently) and the Teams step POSTed to a retired Office 365 connector.

This repo is PUBLIC and every non-admin issue form asks for a Hertie email, so an opened
ticket publishes a student's address. Two things follow, and they are the whole design:

  1. The address leaves the public issue. Once the mail is away the issue body is PATCHed
     with the address replaced by a placeholder.
  2. The order is mail first, redact second, and never the other way round. The ticket is
     the only copy of that address; redacting before a send that then fails would destroy
     it with nothing to show for it. A failed send therefore leaves the body alone and
     fails the run - a red run with the address still there is recoverable, the reverse is
     not.

The mail is a POINTER, not a record. It carries the ticket URL first and says so at the
bottom: the ticket is the single source of truth and nothing replies to this mailbox.

Nothing here prints the address. The run log of a public repo is public, so the address is
masked (`a***@domain`) or reduced to "found"/"not found" wherever it would otherwise appear.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# The mailer is vendored alongside this script; see its docstring for where it comes from.
MAILER = Path(__file__).resolve().parent / "dsl-alert-mail.py"

# Every non-admin issue form labels its address field exactly this. `announcement.yml` is
# admin-only and has no such field, which is why every path here tolerates its absence.
EMAIL_LABEL = "Hertie email"

# What replaces the address in the public issue body. A placeholder rather than a deletion,
# so a reader can tell the field was answered and where the answer went.
REDACTED = "(sent privately to the lab)"

CLOSING = "Reply on the ticket - replies to this email are not tracked."

# GitHub Issue Forms render one answered field as `### <label>` then a blank line then the
# value, so the heading line is the only reliable delimiter. `.+?` swallows a trailing \r
# on a CRLF body; the caller strips it.
_HEADING = re.compile(r"^###[ \t]+(?P<label>.+?)[ \t]*$", re.MULTILINE)

# An unanswered optional field is not omitted - it renders with this as its value.
_NO_RESPONSE = "_No response_"

# Deliberately loose on the local part (people paste `<a@b.org>`, "a@b.org.") and strict on
# the last label, so a trailing period or bracket is not swallowed into the address. Vetting
# the address properly is the mailer's job; this only has to find it.
_ADDRESS = re.compile(r"[^@\s,<>]+@[^@\s,<>]+\.[A-Za-z]{2,}")


def log(msg: str) -> None:
    print(msg, flush=True)


def mask(address: str) -> str:
    """`a***@domain` - enough to tell two addresses apart in a PUBLIC run log, not enough
    to identify either. Same shape the mailer uses, for the same reason."""
    local, _, domain = address.partition("@")
    return f"{local[:1]}***@{domain}" if domain else f"{local[:1]}***"


def field_value(body: str, label: str) -> str | None:
    """The value a form field rendered under `### <label>`, or None if it is not there.

    Returns None for a field left blank as well as one that never existed: an absent
    address and an unanswered one lead to exactly the same behaviour here, so telling them
    apart would only give a caller a distinction it must not act on."""
    body = body or ""
    for match in _HEADING.finditer(body):
        if match.group("label").strip().casefold() != label.casefold():
            continue
        following = _HEADING.search(body, match.end())
        value = body[match.end() : following.start() if following else len(body)].strip()
        return None if not value or value == _NO_RESPONSE else value
    return None


def extract_email(body: str) -> str | None:
    """The address the opener gave, or None.

    Scoped to the address field rather than the whole body on purpose: a ticket routinely
    pastes a traceback, a config file or a docs link, and a body-wide search would send the
    ticket to whatever address happened to be in it and then redact that out of the report."""
    value = field_value(body, EMAIL_LABEL)
    if not value:
        return None
    found = _ADDRESS.search(value)
    return found.group(0) if found else None


def redact(body: str, address: str) -> str:
    """The issue body with every occurrence of `address` replaced by the placeholder.

    Case-insensitive, and not limited to the address field: people repeat their address in
    the free-text boxes, and a redaction that leaves a copy two headings further down has
    done nothing."""
    if not address:
        return body
    return re.sub(re.escape(address), REDACTED, body, flags=re.IGNORECASE)


def compose_subject(number: int, labels: list[str], author: str) -> str:
    """`[ds01-hub #12] bug - someone` - scannable in a mail list without opening anything."""
    return f"[ds01-hub #{number}] {labels[0] if labels else 'Issue'} - {author}"


def compose_body(url: str, issue_body: str) -> str:
    """URL first, ticket text, then the closing line.

    The URL leads because this mail is a pointer: the reader's next action is to open the
    ticket, and it should be the first thing under the subject on a phone."""
    return f"{url}\n\n{(issue_body or '').strip()}\n\n{CLOSING}\n"


def send_mail(subject: str, body: str, cc: str | None) -> bool:
    """Hand the mail to the vendored mailer. True if it reported success.

    The body goes on stdin, per the mailer's contract. `--cc` has to go on argv, which on a
    public runner is only acceptable because the runner is ephemeral and the mailer masks
    the address in everything it logs.

    `--cc` ADDS to DSL_ALERT_CC, so copying the opener cannot displace the archive mailbox."""
    command = [sys.executable, str(MAILER)]
    if cc:
        command += ["--cc", cc]
    command.append(subject)
    return subprocess.run(command, input=body, text=True, check=False).returncode == 0


def patch_issue_body(repo: str, number: int, body: str, token: str) -> bool:
    """PATCH the redacted body back onto the issue. True if GitHub accepted it."""
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues/{number}",
        data=json.dumps({"body": body}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            log(f"issue body redacted ({response.status})")
            return True
    except urllib.error.HTTPError as exc:
        # Status only - a GitHub error body quotes the request, address included.
        log(f"redaction PATCH failed ({exc.code})")
        return False
    except OSError as exc:
        log(f"redaction PATCH failed: {exc.__class__.__name__}")
        return False


def main() -> int:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    issue = event["issue"]
    number = issue["number"]
    body = issue.get("body") or ""
    author = issue["user"]["login"]
    labels = [label["name"] for label in issue.get("labels") or []]

    address = extract_email(body)
    log(f"ticket #{number}: address {mask(address) if address else 'not found'}")

    subject = compose_subject(number, labels, author)
    if not send_mail(subject, compose_body(issue["html_url"], body), address):
        # Deliberately no redaction on this path: see the module docstring.
        log("mail failed - the ticket body is left untouched so the address is not lost")
        return 1

    if not address:
        return 0
    patched = patch_issue_body(
        os.environ["GITHUB_REPOSITORY"],
        number,
        redact(body, address),
        os.environ["GITHUB_TOKEN"],
    )
    # A failed redaction leaves an address on a public issue: red the run so someone looks.
    return 0 if patched else 1


if __name__ == "__main__":
    sys.exit(main())
