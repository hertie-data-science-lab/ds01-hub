#!/usr/bin/env python3
"""ticket_mail.py - the bits every ds01-hub ticket mail must agree on.

Imported by `notify_ticket.py` (new tickets, new comments) and `followup_tickets.py`
(escalations). It holds the two things the two scripts cannot be allowed to disagree about
- the subject line and the rung labels - and the GitHub access they both need to do it.

THREADING is why the subject lives here. Every mail about a ticket has to land in the same
conversation in the reader's mailbox, so that a ticket reads as one thread from "filed"
through every reply to "still open after 7 days". Nothing sets `In-Reply-To` or `References`
here: Graph refuses those headers on a message an application sends, and `internetMessageHeaders`
takes custom `x-` headers only. Graph DOES expose `POST /messages/{id}/reply`, which threads
properly, but replying needs the sent message's id - so a `Mail.Read` grant the lab's app
registration does not have, somewhere to keep an id per ticket, and a change to the vendored
mailer, whose canonical copy lives in ds01-infra. That was judged out of proportion to the
problem. What is left is an IDENTICAL subject, which Exchange keys a conversation on and
which Gmail and Apple Mail fall back to.

So `compose_subject` is load-bearing rather than cosmetic: change it in one caller and that
caller's mail silently starts a second thread, in some clients and not others, with nothing
in the logs to say so.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

API = "https://api.github.com"

CLOSING = "Reply on the ticket - replies to this email are not tracked."

# The escalation rungs' labels, which `followup_tickets.py` applies as its record that a
# rung has been mailed. They live here because BOTH scripts own half the contract:
# followup_tickets applies them, and notify_ticket strips them whenever a comment arrives,
# which is what re-arms the rungs against the new last-activity time. A name that agreed in
# only one of the two places would either escalate a ticket twice or never again.
FOLLOWUP_LABELS = ("followed-up-48h", "followed-up-7d")


def compose_subject(number: int, title: str, author: str) -> str:
    """`[ds01-hub #32] [QUESTION] Access off campus - DreesWo` - the thread key.

    The number leads because it is what makes the subject unique: two tickets can share a
    title, and threading on the title alone would file them together. The title then says
    what the thread is about without opening it, and the opener's login says whose it is.

    Stable for the life of the ticket. It is deliberately built from the issue's own fields
    and nothing about the event - a subject carrying "new comment" or "7 days" would be a
    new subject, and so a new thread, which is exactly what this is here to prevent."""
    return f"[ds01-hub #{number}] {title} - {author}"


def github_api(method: str, url: str, token: str, payload: dict | None = None):
    """One GitHub request, REST or GraphQL, decoded. Raises on anything but success.

    Shared so that the auth header, the API version and the timeout are stated once. Callers
    differ in what they do with a failure - a missed redaction is worth a red run, a label
    that will not come off is not - so this deliberately does no catching of its own."""
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


def newest_comment(repo: str, number: int, count: int, token: str) -> dict | None:
    """The most recent comment on a ticket, or None when it has none.

    `per_page=1&page=<count>` asks for the last page of a one-per-page listing, which is the
    newest comment by itself; the alternative is paging the whole history to read its final
    entry. `count` is the comment count off the issue payload the caller already holds, so a
    ticket nobody has replied to costs no request at all."""
    if not count:
        return None
    query = urllib.parse.urlencode({"per_page": 1, "page": count})
    page = github_api("GET", f"{API}/repos/{repo}/issues/{number}/comments?{query}", token) or []
    return page[-1] if page else None
