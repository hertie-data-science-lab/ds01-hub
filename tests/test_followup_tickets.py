"""Unit tests for the stale-ticket reminder.

The network is touched in one place only - `last_activity` asks GitHub for a ticket's newest
comment - and that is stubbed. Everything else is pure, which is deliberately where the logic
lives. What is asserted is which rung a ticket has reached, that a rung fires once, that the
loudest rung wins, and that a ticket somebody has just replied to goes quiet again: the four
ways this could go wrong without anybody noticing.
"""

import importlib.util
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / ".github" / "scripts"
SCRIPT = SCRIPTS / "followup_tickets.py"

NOW = datetime(2026, 9, 16, 12, 0, 0, tzinfo=UTC)


@pytest.fixture(scope="module")
def mod():
    # The scripts directory has to be importable, not just the file: followup_tickets shares
    # its subject line and its label names with notify_ticket through ticket_mail.
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("followup_tickets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def stamp(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def ticket(hours_old=1, labels=(), number=1, comments=0):
    return {
        "number": number,
        "title": "GPU quota",
        "html_url": f"https://github.com/o/r/issues/{number}",
        "user": {"login": "someone"},
        "created_at": stamp(NOW - timedelta(hours=hours_old)),
        "labels": [{"name": n} for n in labels],
        "comments": comments,
    }


def idle(hours):
    return hours * 3600


# ------------------------------------------------------------------- which rung is due


def test_a_fresh_ticket_is_left_alone(mod):
    assert mod.due_rung(ticket(), idle(1)) is None


def test_a_ticket_just_short_of_48h_is_left_alone(mod):
    assert mod.due_rung(ticket(47.9), idle(47.9)) is None


def test_48h_exactly_is_due(mod):
    # The boundary is inclusive: a ticket that has been quiet for exactly 48h has reached it.
    assert mod.due_rung(ticket(48), idle(48)) == ("followed-up-48h", "no activity for 48 hours")


def test_7d_is_due(mod):
    assert mod.due_rung(ticket(24 * 7), idle(24 * 7)) == (
        "followed-up-7d",
        "no activity for 7 days",
    )


# --------------------------------------------------------------- measured from activity


def test_an_old_ticket_that_was_just_answered_is_left_alone(mod):
    # The point of the change: a month-old ticket somebody replied to an hour ago is being
    # handled, and chasing it would be noise.
    assert mod.due_rung(ticket(24 * 30), idle(1)) is None


def test_a_ticket_that_went_quiet_again_is_chased_again(mod):
    # The rung labels are stripped by notify_ticket when a comment arrives, so a ticket that
    # was answered and then ignored for two days is due once more.
    assert mod.due_rung(ticket(24 * 30), idle(48)) == (
        "followed-up-48h",
        "no activity for 48 hours",
    )


# --------------------------------------------------------------------------- once only


def test_a_labelled_rung_never_fires_again(mod):
    assert mod.due_rung(ticket(60, labels=["followed-up-48h"]), idle(60)) is None


def test_the_48h_label_does_not_suppress_the_7d_rung(mod):
    # The whole point of separate labels: a ticket goes quiet after 48h and speaks again
    # at a week.
    assert mod.due_rung(ticket(24 * 8, labels=["followed-up-48h"]), idle(24 * 8)) == (
        "followed-up-7d",
        "no activity for 7 days",
    )


def test_a_ticket_past_both_rungs_reports_the_louder_one(mod):
    # A schedule that did not fire for five days must say "7 days", not "48 hours" and then
    # the real news three hours later.
    assert mod.due_rung(ticket(24 * 9), idle(24 * 9))[0] == "followed-up-7d"


def test_a_fully_labelled_ticket_is_silent(mod):
    stale = ticket(24 * 30, labels=["followed-up-48h", "followed-up-7d"])
    assert mod.due_rung(stale, idle(24 * 30)) is None


# ----------------------------------------------------------------------- last activity


def test_a_ticket_with_no_comments_is_measured_from_when_it_was_filed(mod, monkeypatch):
    monkeypatch.setattr(mod, "newest_comment", lambda *_a, **_k: None)
    assert mod.last_activity(ticket(48), "o/r", "tok") == NOW - timedelta(hours=48)


def test_a_commented_ticket_is_measured_from_its_newest_comment(mod, monkeypatch):
    replied = NOW - timedelta(hours=2)
    monkeypatch.setattr(mod, "newest_comment", lambda *_a, **_k: {"created_at": stamp(replied)})
    assert mod.last_activity(ticket(24 * 30, comments=3), "o/r", "tok") == replied


def test_the_clock_is_githubs_not_the_runners(mod, monkeypatch):
    monkeypatch.setattr(mod, "newest_comment", lambda *_a, **_k: None)
    assert mod.last_activity(ticket(48), "o/r", "tok") == NOW - timedelta(hours=48)


# --------------------------------------------------------------- what a run bothers to ask


def test_a_fully_escalated_ticket_is_not_asked_about_again(mod, monkeypatch):
    """It stays open for months and has nothing left to say, so it must not cost a request
    on every run of a three-hourly cron."""

    def fail(*_args, **_kwargs):
        raise AssertionError("a fully escalated ticket must not be asked about")

    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("GITHUB_TOKEN", "tok")
    stale = ticket(24 * 90, labels=["followed-up-48h", "followed-up-7d"], comments=4)
    monkeypatch.setattr(mod, "open_tickets", lambda *_a, **_k: [stale])
    monkeypatch.setattr(mod, "newest_comment", fail)
    monkeypatch.setattr(mod, "send", fail)
    assert mod.main() == 0


def test_a_ticket_younger_than_every_rung_is_not_asked_about(mod, monkeypatch):
    def fail(*_args, **_kwargs):
        raise AssertionError("a fresh ticket must not be asked about")

    # Against the real clock, because `main` reads it: a ticket pinned to this module's
    # fixed NOW would age past the 48h rung as the calendar moved and fail some Tuesday.
    fresh = ticket(2, comments=1)
    fresh["created_at"] = stamp(datetime.now(UTC) - timedelta(hours=2))
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("GITHUB_TOKEN", "tok")
    monkeypatch.setattr(mod, "open_tickets", lambda *_a, **_k: [fresh])
    monkeypatch.setattr(mod, "newest_comment", fail)
    monkeypatch.setattr(mod, "send", fail)
    assert mod.main() == 0


# ------------------------------------------------------------------------- the message


def test_the_body_leads_with_the_ticket_url(mod):
    # The link is the first thing in the mail, whatever the body format: the only useful
    # next action is to open the ticket.
    _subject, body = mod.compose(ticket(48, labels=["bug"]), "no activity for 48 hours")
    assert body.splitlines()[0].startswith("<p><a href=")
    assert "https://github.com/o/r/issues/1" in body.splitlines()[0]


def test_the_subject_is_the_tickets_subject_not_the_rungs(mod):
    # Identical to the subject the opening mail and every comment mail carries - that is the
    # only thing keeping them in one thread.
    subject, _body = mod.compose(ticket(48, labels=["bug"]), "no activity for 48 hours")
    assert subject == "[ds01-hub #1] GPU quota - someone"


def test_both_rungs_share_one_subject(mod):
    first, _ = mod.compose(ticket(48), "no activity for 48 hours")
    second, _ = mod.compose(ticket(24 * 7), "no activity for 7 days")
    assert first == second


def test_what_the_reminder_says_lives_in_the_body(mod):
    _subject, body = mod.compose(ticket(48), "no activity for 48 hours")
    assert "no activity for 48 hours" in body


def test_the_body_says_replies_are_not_tracked(mod):
    _subject, body = mod.compose(ticket(48), "no activity for 48 hours")
    assert "Reply on the ticket" in body


# ------------------------------------------------------------------------ HTML bodies


def test_the_reminder_links_the_ticket_rather_than_printing_a_url(mod):
    _subject, body = mod.compose(ticket(48, labels=["bug"]), "no activity for 48 hours")
    assert '<a href="https://github.com/o/r/issues/1">' in body


def test_a_title_cannot_inject_html(mod):
    # The title is whatever a stranger typed into a public form, and it lands in a mail
    # client that will render what it is given.
    hostile = ticket(48)
    hostile["title"] = '<script>alert("x")</script> & "quoted"'
    _subject, body = mod.compose(hostile, "no activity for 48 hours")
    assert "<script>" not in body
    assert "&lt;script&gt;" in body
    assert "&amp;" in body


def test_the_login_is_escaped_too(mod):
    odd = ticket(48)
    odd["user"]["login"] = "a<b>c"
    _subject, body = mod.compose(odd, "no activity for 48 hours")
    assert "<b>" not in body
