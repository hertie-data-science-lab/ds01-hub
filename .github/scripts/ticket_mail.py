#!/usr/bin/env python3
"""ticket_mail.py - the bits every ds01-hub ticket mail must agree on.

Imported by `notify_ticket.py` (new tickets, new comments) and `followup_tickets.py`
(escalations). It exists for one reason: THREADING.

Every mail about a ticket has to land in the same conversation in the reader's mailbox, so
that a ticket reads as one thread from "filed" through every reply to "still open after 7
days". Nothing sets `In-Reply-To` or `References` here - Graph does not let an application
set those headers on a message it sends - so the only thing holding the thread together is
an IDENTICAL subject line. Exchange keys a conversation on the normalised subject, and
Gmail and Apple Mail fall back to the same heuristic.

That makes `compose_subject` load-bearing rather than cosmetic: change it in one caller and
that caller's mail silently starts a second thread. It lives here so there is one copy.
"""

from __future__ import annotations

CLOSING = "Reply on the ticket - replies to this email are not tracked."


def compose_subject(number: int, title: str, author: str) -> str:
    """`[ds01-hub #32] [QUESTION] Access off campus - DreesWo` - the thread key.

    The number leads because it is what makes the subject unique: two tickets can share a
    title, and threading on the title alone would file them together. The title then says
    what the thread is about without opening it, and the opener's login says whose it is.

    Stable for the life of the ticket. It is deliberately built from the issue's own fields
    and nothing about the event - a subject carrying "new comment" or "7 days" would be a
    new subject, and so a new thread, which is exactly what this is here to prevent."""
    return f"[ds01-hub #{number}] {title} - {author}"


# The escalation rungs' labels, which `followup_tickets.py` applies as its record that a
# rung has been mailed. They live here because BOTH scripts own half the contract:
# followup_tickets applies them, and notify_ticket strips them whenever a comment arrives,
# which is what re-arms the rungs against the new last-activity time. A name that agrees in
# only one of the two places would either escalate a ticket twice or never again.
FOLLOWUP_LABELS = ("followed-up-48h", "followed-up-7d")
