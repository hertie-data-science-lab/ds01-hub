#!/usr/bin/env python3
"""notify_ticket.py - mail the lab about a ds01-hub ticket: a new one, or a new comment.

Run by `.github/workflows/notify-ticket.yml` on `issues: [opened]` and on
`issue_comment: [created]`. Before this existed a filed ticket notified nobody: the assignee
was a login the repo cannot assign (GitHub drops those silently) and the Teams step POSTed
to a retired Office 365 connector.

Two paths, and they differ in more than their wording:

NEW TICKET. This repo is PUBLIC and every non-admin issue form asks for a Hertie email, so
an opened ticket publishes a student's address. Two things follow, and they are the whole
design:

  1. The address leaves the public issue. Once the mail is away the issue body is PATCHed
     with the address replaced by a placeholder.
  2. The order is mail first, redact second, and never the other way round. The ticket is
     the only copy of that address; redacting before a send that then fails would destroy
     it with nothing to show for it. A failed send therefore leaves the body alone and
     fails the run - a red run with the address still there is recoverable, the reverse is
     not.

NEW COMMENT. The same mail, about the comment, to the same three places, under the same
subject - so a ticket reads as ONE mail thread from "filed" to "closed" rather than an
opening mail and then silence. See `ticket_mail.compose_subject`: the subject is the only
thing holding that thread together.

A comment also RESETS THE ESCALATION CLOCK, by stripping the rungs' labels off the ticket.
`followup_tickets.py` measures from the last activity, and its labels are its record of
what it has already said; a ticket somebody has just replied to has to be able to go quiet
and then escalate again.

Reaching the opener on a comment needs an address the new-ticket path has already redacted
out of the body, so it is read back from the issue's first revision - see `opener_address`.

The mail is a POINTER, not a record. It carries the ticket URL first and says so at the
bottom: the ticket is the single source of truth and nothing replies to this mailbox.

Nothing here prints the address. The run log of a public repo is public, so the address is
masked (`a***@domain`) or reduced to "found"/"not found" wherever it would otherwise appear.
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from ticket_mail import (
    API,
    CLOSING,
    FOLLOWUP_LABELS,
    compose_subject,
    github_api,
    newest_comment,
)

# The mailer is vendored alongside this script; see its docstring for where it comes from.
MAILER = Path(__file__).resolve().parent / "dsl-alert-mail.py"

# Every non-admin issue form labels its address field exactly this. `announcement.yml` is
# admin-only and has no such field, which is why every path here tolerates its absence.
EMAIL_LABEL = "Hertie email"

# What replaces the address in the public issue body. A placeholder rather than a deletion,
# so a reader can tell the field was answered and where the answer went.
REDACTED = "(sent privately to the lab)"

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


def first_revision_body(repo: str, number: int, token: str) -> str | None:
    """The issue body as it was FIRST submitted, out of GitHub's edit history, or None.

    GitHub keeps every revision of an issue body and serves them through GraphQL, so the
    redaction this script performs is reversible - by us here, and by anyone else with a
    token, which is worth knowing independently of this function. The field is named `diff`
    but holds the FULL body at that revision, not a patch, so it can be handed straight to
    the same field parser as a live body.

    Earliest revision by `editedAt`, not whatever order the API returned, and never the
    newest: the newest is the redaction itself and its address field says `(sent privately
    to the lab)`.

    `diff` is null for a viewer without push access. GITHUB_TOKEN in Actions has it, but the
    day that changes this returns None and the caller mails the lab without the opener,
    which is the right way round to fail."""
    owner, _, name = repo.partition("/")
    query = """
      query($owner: String!, $name: String!, $number: Int!) {
        repository(owner: $owner, name: $name) {
          issue(number: $number) {
            userContentEdits(first: 50) { nodes { editedAt diff } }
          }
        }
      }
    """
    try:
        result = github_api(
            "POST",
            f"{API}/graphql",
            token,
            {"query": query, "variables": {"owner": owner, "name": name, "number": number}},
        )
    except (urllib.error.HTTPError, OSError) as exc:
        code = getattr(exc, "code", exc.__class__.__name__)
        log(f"edit history lookup failed ({code})")
        return None

    # GraphQL reports a bad query as 200 plus an `errors` key, so a missing path here is not
    # exceptional and must not raise.
    issue = ((result or {}).get("data") or {}).get("repository", {}).get("issue")
    nodes = [
        n for n in ((issue or {}).get("userContentEdits") or {}).get("nodes") or [] if n.get("diff")
    ]
    if not nodes:
        return None
    return min(nodes, key=lambda n: n["editedAt"])["diff"]


def opener_address(repo: str, number: int, body: str, token: str) -> str | None:
    """The address of whoever filed the ticket, for the Cc line.

    The live body first - on a ticket whose redaction never ran, or one filed before this
    workflow existed, the address is still sitting in it and no second request is needed.
    Only then the first revision, which is where the address goes once this script has done
    its job."""
    address = extract_email(body)
    if address:
        return address
    original = first_revision_body(repo, number, token)
    return extract_email(original) if original else None


def render_markdown(body: str, repo: str, token: str) -> str | None:
    """A markdown body as HTML, rendered by GitHub itself, or None if that fails.

    GitHub renders it rather than this script, for two reasons. An issue form body is
    GitHub-Flavoured Markdown - `### heading`, fenced code, task lists, autolinked #refs -
    and reimplementing a subset here would render some tickets correctly and others
    misleadingly. And the endpoint SANITISES: the body is whatever a stranger typed into a
    public form, and it arrives in a mail client that will happily run what it is given.

    None on any failure, and the caller falls back to plain text. A mail that reads like
    raw markdown is a cosmetic problem; a mail that never arrives is the actual fault."""
    request = urllib.request.Request(
        f"{API}/markdown",
        data=json.dumps({"text": body, "mode": "gfm", "context": repo}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode()
    except (urllib.error.HTTPError, OSError, UnicodeDecodeError) as exc:
        code = getattr(exc, "code", exc.__class__.__name__)
        log(f"markdown render failed ({code}) - falling back to plain text")
        return None


def compose_body(url: str, issue_body: str, lead: str = "") -> str:
    """The plain-text mail: URL first, the text, then the closing line.

    The URL leads because this mail is a pointer: the reader's next action is to open the
    ticket, and it should be the first thing under the subject on a phone."""
    opening = f"{url}\n\n{lead}\n" if lead else f"{url}\n"
    return f"{opening}\n{(issue_body or '').strip()}\n\n{CLOSING}\n"


def compose_html(url: str, rendered: str, lead: str = "") -> str:
    """The HTML mail: the same shape, around GitHub's rendering of the text.

    No stylesheet and no layout. This is read in Outlook, in a phone client and in a shared
    mailbox, and the one thing every one of them agrees on is a plain document. The only
    rule kept from the text version is that the link comes first."""
    link = html.escape(url, quote=True)
    heading = f"<p><strong>{html.escape(lead)}</strong></p>\n" if lead else ""
    return (
        f'<p><a href="{link}">{html.escape(url)}</a></p>\n'
        f"{heading}"
        f"<hr>\n{rendered}\n<hr>\n"
        f"<p><em>{html.escape(CLOSING)}</em></p>\n"
    )


def send_mail(subject: str, body: str, cc: str | None, *, as_html: bool = False) -> bool:
    """Hand the mail to the vendored mailer. True if it reported success.

    The body goes on stdin, per the mailer's contract. `--cc` has to go on argv, which on a
    public runner is only acceptable because the runner is ephemeral and the mailer masks
    the address in everything it logs.

    `--cc` ADDS to DSL_ALERT_CC, so copying the opener cannot displace the archive mailbox."""
    command = [sys.executable, str(MAILER)]
    if as_html:
        command.append("--html")
    if cc:
        command += ["--cc", cc]
    command.append(subject)
    return subprocess.run(command, input=body, text=True, check=False).returncode == 0


def mail_rendered(
    subject: str, url: str, text: str, cc: str | None, repo: str, token: str, lead: str = ""
) -> bool:
    """Send `text` as HTML when GitHub will render it, as plain text when it will not.

    The body of an issue or a comment is markdown, so as text it reads as `### Hertie email`
    rather than a heading - legible, but plainly a machine's idea of a mail."""
    rendered = render_markdown(text, repo, token)
    if rendered is None:
        return send_mail(subject, compose_body(url, text, lead), cc)
    return send_mail(subject, compose_html(url, rendered, lead), cc, as_html=True)


def patch_issue_body(repo: str, number: int, body: str, token: str) -> bool:
    """PATCH the redacted body back onto the issue. True if GitHub accepted it."""
    try:
        github_api("PATCH", f"{API}/repos/{repo}/issues/{number}", token, {"body": body})
        log("issue body redacted")
        return True
    except urllib.error.HTTPError as exc:
        # Status only - a GitHub error body quotes the request, address included.
        log(f"redaction PATCH failed ({exc.code})")
        return False
    except OSError as exc:
        log(f"redaction PATCH failed: {exc.__class__.__name__}")
        return False


def reset_followup_rungs(repo: str, number: int, token: str) -> None:
    """Strip the escalation labels, so the rungs can fire again from this comment.

    Best effort on purpose. A label that will not come off means the ticket is not chased
    again until the next comment, which is a quieter failure than an unsent mail and not
    worth reddening a run that has already delivered the thing it exists to deliver. A 404
    is the ordinary case - most tickets never reach a rung."""
    for name in FOLLOWUP_LABELS:
        try:
            github_api(
                "DELETE",
                f"{API}/repos/{repo}/issues/{number}/labels/{urllib.parse.quote(name)}",
                token,
            )
            log(f"cleared {name}")
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                log(f"could not clear {name} ({exc.code})")
        except OSError as exc:
            log(f"could not clear {name}: {exc.__class__.__name__}")


def handle_opened(issue: dict, repo: str, token: str) -> int:
    """A newly filed ticket: mail it, then take the address out of the public body."""
    number = issue["number"]
    body = issue.get("body") or ""

    address = extract_email(body)
    log(f"ticket #{number}: address {mask(address) if address else 'not found'}")

    subject = compose_subject(number, issue["title"], issue["user"]["login"])
    if not mail_rendered(subject, issue["html_url"], body, address, repo, token):
        # Deliberately no redaction on this path: see the module docstring.
        log("mail failed - the ticket body is left untouched so the address is not lost")
        return 1

    if not address:
        return 0
    patched = patch_issue_body(repo, number, redact(body, address), token)
    # A failed redaction leaves an address on a public issue: red the run so someone looks.
    return 0 if patched else 1


def handle_comment(issue: dict, comment: dict, repo: str, token: str) -> int:
    """A new comment: mail it into the ticket's thread and re-arm the escalation rungs.

    The rungs are reset whether or not the mail got out. The clock measures when the ticket
    was last touched, which is a fact about the ticket and not about our mail channel."""
    number = issue["number"]
    commenter = comment["user"]["login"]

    address = opener_address(repo, number, issue.get("body") or "", token)
    log(f"comment on #{number} by {commenter}: address {mask(address) if address else 'not found'}")

    subject = compose_subject(number, issue["title"], issue["user"]["login"])
    lead = f"New comment from {commenter}"
    sent = mail_rendered(
        subject, comment["html_url"], comment.get("body") or "", address, repo, token, lead
    )

    reset_followup_rungs(repo, number, token)
    if not sent:
        log("comment mail failed")
        return 1
    return 0


def handle_backfill(number: int, repo: str, token: str) -> int:
    """Mail a ticket's newest comment on demand, for a comment no event ever covered.

    Two uses, and the second is the reason it is worth having. A comment made before this
    workflow learned about comments at all is only in the ticket, and mailing it puts the
    record where the rest of the record is. And a comment mail that FAILS is not retried by
    anything - the event is gone - so this is the way to send it after the fault is fixed.

    Sends into whatever thread the ticket's subject names now. A ticket whose opening mail
    went out under an older subject will therefore start a fresh thread rather than join the
    old one, which is a cosmetic price paid once."""
    issue = github_api("GET", f"{API}/repos/{repo}/issues/{number}", token)
    newest = newest_comment(repo, number, (issue or {}).get("comments") or 0, token)
    if newest is None:
        log(f"#{number} has no comments to mail")
        return 1
    log(f"backfilling the newest comment on #{number}")
    return handle_comment(issue, newest, repo, token)


def main() -> int:
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]

    # A manual run names a ticket instead of carrying an event, so it is settled before the
    # event file is read - `workflow_dispatch` writes one, but it holds no issue.
    backfill = (os.environ.get("BACKFILL_ISSUE") or "").strip()
    if backfill:
        return handle_backfill(int(backfill), repo, token)

    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    issue = event["issue"]

    # The presence of `comment` is what distinguishes the two events; the workflow already
    # refuses everything except `issues: opened` and `issue_comment: created`.
    comment = event.get("comment")
    if comment:
        return handle_comment(issue, comment, repo, token)
    return handle_opened(issue, repo, token)


if __name__ == "__main__":
    sys.exit(main())
