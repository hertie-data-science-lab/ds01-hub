#!/usr/bin/env python3
"""followup_tickets.py - mail the lab about tickets that have been open too long.

Run on a schedule by `.github/workflows/ticket-followup.yml`. A ticket that nobody has
closed after FOLLOWUP_RUNGS is one the lab has not finished with, and the opener was told
when they filed it that the ticket is the record - so the reminder goes to the lab, not
back to them. Being chased about your own unanswered request helps nobody.

IDEMPOTENT THROUGH LABELS, not through state kept anywhere else. Each rung applies its own
label when it mails, and a labelled ticket is never mailed for that rung again. The label is
the record, it is visible on the ticket to anyone triaging, and it survives a re-run, a
replayed schedule and a workflow that is edited underneath it. GitHub delivers a `schedule:`
trigger unreliably - measured at a few percent on a busy cron - so this is written to be
late rather than wrong: a missed fire delivers the reminder on the next one, and a rung
whose label is already there stays quiet forever.

Rungs are checked LOUDEST FIRST and at most one mail is sent per ticket per run. A ticket
that sat through both thresholds while nothing fired should say "7 days", not "48 hours"
followed by the real news an hour later.

Nothing here prints an address; this repo is PUBLIC and so is the run log.
"""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

MAILER = Path(__file__).resolve().parent / "dsl-alert-mail.py"

API = "https://api.github.com"

# Age, the label that proves this rung was mailed, and how the subject says it. Ordered
# loudest first; the first match wins, so a new rung goes in age order.
FOLLOWUP_RUNGS = (
    (7 * 24 * 3600, "followed-up-7d", "still open after 7 days"),
    (48 * 3600, "followed-up-48h", "still open after 48 hours"),
)

CLOSING = "Reply on the ticket - replies to this email are not tracked."


def log(msg: str) -> None:
    print(msg, flush=True)


def _request(method: str, url: str, token: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Content-Type": "application/json"} if data else {}),
        },
        method=method,
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


def open_tickets(repo: str, token: str) -> list[dict]:
    """Every open issue in the repo, pull requests excluded.

    `/issues` returns PRs as well - they carry a `pull_request` key - and a PR left open for
    a week is not a ticket anybody filed."""
    tickets: list[dict] = []
    page = 1
    while True:
        query = urllib.parse.urlencode({"state": "open", "per_page": 100, "page": page})
        batch = _request("GET", f"{API}/repos/{repo}/issues?{query}", token) or []
        tickets += [issue for issue in batch if "pull_request" not in issue]
        if len(batch) < 100:
            return tickets
        page += 1


def age_seconds(issue: dict, now: datetime) -> float:
    """How long the ticket has been open, from GitHub's own `created_at`.

    The API clock, never the runner's: a runner that queued for twenty minutes would
    otherwise read every ticket as twenty minutes older than it is."""
    created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
    return (now - created).total_seconds()


def due_rung(issue: dict, now: datetime) -> tuple[str, str] | None:
    """The (label, phrase) of the loudest rung this ticket has reached and not been mailed
    for, or None if there is nothing to say about it."""
    labels = {label["name"] for label in issue.get("labels") or []}
    age = age_seconds(issue, now)
    for threshold, label, phrase in FOLLOWUP_RUNGS:
        if age >= threshold and label not in labels:
            return label, phrase
    return None


def compose(issue: dict, phrase: str) -> tuple[str, str]:
    """The subject and HTML body of one reminder.

    HTML, not text, so the ticket is a link the reader can press rather than a URL they have
    to select - this mail exists to get somebody back to the ticket. Nothing is rendered
    from the ticket itself, so there is no markdown to handle: the title is the only
    attacker-supplied value and it is escaped."""
    kind = (issue.get("labels") or [{}])[0].get("name", "Issue")
    subject = f"[ds01-hub #{issue['number']}] {phrase} - {kind}"
    url = html.escape(issue["html_url"], quote=True)
    body = (
        f'<p><a href="{url}">{html.escape(issue["html_url"])}</a></p>\n'
        f"<p><strong>{html.escape(issue['title'])}</strong><br>\n"
        f"Opened by {html.escape(issue['user']['login'])} "
        f"on {html.escape(issue['created_at'][:10])}.</p>\n"
        f"<p>This ticket is {html.escape(phrase.replace('still open after ', 'now '))} old "
        f"and is still open.</p>\n"
        f"<p><em>{html.escape(CLOSING)}</em></p>\n"
    )
    return subject, body


def send(subject: str, body: str) -> bool:
    """Hand one reminder to the vendored mailer. Recipients come entirely from the
    environment - no `--cc` here, because a reminder goes to the lab and never to the
    person who filed the ticket."""
    return (
        subprocess.run(
            [sys.executable, str(MAILER), "--html", subject],
            input=body,
            text=True,
            check=False,
        ).returncode
        == 0
    )


def label(repo: str, number: int, name: str, token: str) -> bool:
    """Record that this rung was mailed. Applied only AFTER a successful send, so a failed
    mail is retried on the next run instead of being silently marked done."""
    try:
        _request("POST", f"{API}/repos/{repo}/issues/{number}/labels", token, {"labels": [name]})
        return True
    except (urllib.error.HTTPError, OSError) as exc:
        code = getattr(exc, "code", exc.__class__.__name__)
        log(f"  #{number}: labelling failed ({code}) - will re-mail next run")
        return False


def main() -> int:
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]
    now = datetime.now(UTC)

    tickets = open_tickets(repo, token)
    log(f"{len(tickets)} open ticket(s)")

    mailed = failed = 0
    for issue in sorted(tickets, key=lambda i: i["number"]):
        rung = due_rung(issue, now)
        if rung is None:
            continue
        name, phrase = rung
        subject, body = compose(issue, phrase)
        if not send(subject, body):
            log(f"  #{issue['number']}: mail failed - not labelled, will retry")
            failed += 1
            continue
        mailed += 1
        log(f"  #{issue['number']}: {phrase}")
        label(repo, issue["number"], name, token)

    log(f"mailed {mailed}, failed {failed}")
    # A failed reminder is worth a red run: the ticket stays unlabelled and will be retried,
    # but a mail channel that has stopped working should not look healthy.
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
