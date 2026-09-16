"""Unit tests for the stale-ticket reminder.

The network is never touched: `due_rung` and `compose` are pure, and that is deliberately
where all the logic lives. What is asserted is which rung a ticket has reached, that a rung
fires once, and that the loudest rung wins - the three ways this could quietly go wrong.
"""

import importlib.util
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / ".github/scripts/followup_tickets.py"

NOW = datetime(2026, 9, 16, 12, 0, 0, tzinfo=UTC)


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("followup_tickets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ticket(hours_old, labels=(), number=1):
    created = NOW - timedelta(hours=hours_old)
    return {
        "number": number,
        "title": "GPU quota",
        "html_url": f"https://github.com/o/r/issues/{number}",
        "user": {"login": "someone"},
        "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "labels": [{"name": n} for n in labels],
    }


# ------------------------------------------------------------------- which rung is due


def test_a_fresh_ticket_is_left_alone(mod):
    assert mod.due_rung(ticket(1), NOW) is None


def test_a_ticket_just_short_of_48h_is_left_alone(mod):
    assert mod.due_rung(ticket(47.9), NOW) is None


def test_48h_exactly_is_due(mod):
    # The boundary is inclusive: a ticket that is exactly 48h old has reached the rung.
    assert mod.due_rung(ticket(48), NOW) == ("followed-up-48h", "still open after 48 hours")


def test_7d_is_due(mod):
    assert mod.due_rung(ticket(24 * 7), NOW) == ("followed-up-7d", "still open after 7 days")


# --------------------------------------------------------------------------- once only


def test_a_labelled_rung_never_fires_again(mod):
    assert mod.due_rung(ticket(60, labels=["followed-up-48h"]), NOW) is None


def test_the_48h_label_does_not_suppress_the_7d_rung(mod):
    # The whole point of separate labels: a ticket goes quiet after 48h and speaks again
    # at a week.
    assert mod.due_rung(ticket(24 * 8, labels=["followed-up-48h"]), NOW) == (
        "followed-up-7d",
        "still open after 7 days",
    )


def test_a_ticket_past_both_rungs_reports_the_louder_one(mod):
    # A schedule that did not fire for five days must say "7 days", not "48 hours" and then
    # the real news three hours later.
    assert mod.due_rung(ticket(24 * 9), NOW)[0] == "followed-up-7d"


def test_a_fully_labelled_ticket_is_silent(mod):
    stale = ticket(24 * 30, labels=["followed-up-48h", "followed-up-7d"])
    assert mod.due_rung(stale, NOW) is None


# ------------------------------------------------------------------------- the message


def test_the_body_leads_with_the_ticket_url(mod):
    # The link is the first thing in the mail, whatever the body format: the only useful
    # next action is to open the ticket.
    _subject, body = mod.compose(ticket(48, labels=["bug"]), "still open after 48 hours")
    assert body.splitlines()[0].startswith("<p><a href=")
    assert "https://github.com/o/r/issues/1" in body.splitlines()[0]


def test_the_subject_carries_the_number_and_the_rung(mod):
    subject, _body = mod.compose(ticket(48, labels=["bug"]), "still open after 48 hours")
    assert subject == "[ds01-hub #1] still open after 48 hours - bug"


def test_an_unlabelled_ticket_still_composes(mod):
    subject, _body = mod.compose(ticket(48), "still open after 48 hours")
    assert subject.endswith("- Issue")


def test_the_body_says_replies_are_not_tracked(mod):
    _subject, body = mod.compose(ticket(48), "still open after 48 hours")
    assert "Reply on the ticket" in body


# -------------------------------------------------------------------------------- age


def test_age_is_measured_from_githubs_clock_not_the_runners(mod):
    assert mod.age_seconds(ticket(48), NOW) == pytest.approx(48 * 3600)


# ------------------------------------------------------------------------ HTML bodies


def test_the_reminder_links_the_ticket_rather_than_printing_a_url(mod):
    _subject, body = mod.compose(ticket(48, labels=["bug"]), "still open after 48 hours")
    assert '<a href="https://github.com/o/r/issues/1">' in body


def test_a_title_cannot_inject_html(mod):
    # The title is whatever a stranger typed into a public form, and it lands in a mail
    # client that will render what it is given.
    hostile = ticket(48)
    hostile["title"] = '<script>alert("x")</script> & "quoted"'
    _subject, body = mod.compose(hostile, "still open after 48 hours")
    assert "<script>" not in body
    assert "&lt;script&gt;" in body
    assert "&amp;" in body


def test_the_login_is_escaped_too(mod):
    odd = ticket(48)
    odd["user"]["login"] = "a<b>c"
    _subject, body = mod.compose(odd, "still open after 48 hours")
    assert "<b>" not in body
