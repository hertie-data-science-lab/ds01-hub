"""Tests for the ticket notifier's parsing and redaction.

This is the risky half of `.github/workflows/notify-ticket.yml`: it decides what counts as
a student's email address on a PUBLIC repo, and it rewrites the issue body afterwards. A
parser that misses the field silently un-copies the person who filed the ticket AND leaves
their address published; one that matches too eagerly mails the ticket to whatever address
was pasted into a traceback.

The bodies below are the shape GitHub Issue Forms actually render - taken from the rendered
form of a real ds01-hub ticket, with a made-up address substituted.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

import notify_ticket
from notify_ticket import (
    REDACTED,
    compose_body,
    compose_html,
    extract_email,
    field_value,
    first_revision_body,
    mask,
    opener_address,
    redact,
    render_markdown,
    send_mail,
)
from ticket_mail import compose_subject

# The rendered shape of access_request.yml, verbatim apart from the address.
ACCESS_REQUEST = (
    "### Hertie email\n"
    "\n"
    "a.student@students.hertie-school.org\n"
    "\n"
    "### Type of request\n"
    "\n"
    "ds01 GPU Server Access\n"
    "\n"
    "### What do you need?\n"
    "\n"
    "I need access to ds01 for working on my masters thesis.\n"
    "\n"
    "### Access needed until\n"
    "\n"
    "30-06-2027\n"
    "\n"
    "### Any installation instructions or links?\n"
    "\n"
    "_No response_\n"
)

# announcement.yml is admin-only and has no address field at all.
ANNOUNCEMENT = (
    "### Announcement type\n\nScheduled Maintenance\n\n### When?\n\nDec 5, 2026, 6pm-8pm CET\n"
)


def test_extracts_the_address_from_a_real_form_body():
    assert extract_email(ACCESS_REQUEST) == "a.student@students.hertie-school.org"


def test_a_template_without_an_email_field_yields_none():
    assert extract_email(ANNOUNCEMENT) is None


def test_a_crlf_body_parses():
    assert extract_email(ACCESS_REQUEST.replace("\n", "\r\n")) == (
        "a.student@students.hertie-school.org"
    )


def test_an_unanswered_field_yields_none():
    body = "### Hertie email\n\n_No response_\n\n### Topic\n\nGPUs\n"
    assert extract_email(body) is None


def test_an_empty_field_yields_none():
    assert extract_email("### Hertie email\n\n\n### Topic\n\nGPUs\n") is None


def test_a_body_that_is_not_a_form_yields_none():
    assert extract_email("ssh is broken, mail me at a.student@hertie-school.org") is None


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("<a.student@hertie-school.org>", "a.student@hertie-school.org"),
        ("a.student@hertie-school.org.", "a.student@hertie-school.org"),
        ("my email is a.student@hertie-school.org", "a.student@hertie-school.org"),
        ("  a.student@hertie-school.org  ", "a.student@hertie-school.org"),
    ],
)
def test_tolerates_how_people_actually_type_an_address(value, expected):
    assert extract_email(f"### Hertie email\n\n{value}\n\n### Topic\n\nGPUs\n") == expected


def test_a_field_with_no_address_in_it_yields_none():
    assert extract_email("### Hertie email\n\nn/a\n\n### Topic\n\nGPUs\n") is None


def test_only_the_email_field_is_searched():
    """A traceback or a config paste must not become the Cc recipient."""
    body = (
        "### Hertie email\n\nn/a\n\n### Error message / output\n\nSMTP to ops@example.com refused\n"
    )
    assert extract_email(body) is None


def test_field_value_is_case_insensitive_on_the_label():
    assert field_value("### hertie EMAIL\n\nx\n", "Hertie email") == "x"


def test_redaction_removes_every_copy_of_the_address():
    body = ACCESS_REQUEST.replace(
        "I need access", "Mail a.student@students.hertie-school.org - I need access"
    )
    address = extract_email(body)
    out = redact(body, address)
    assert address not in out
    assert out.count(REDACTED) == 2


def test_redaction_is_case_insensitive():
    body = "### Hertie email\n\nA.Student@Hertie-School.org\n"
    out = redact(body, "a.student@hertie-school.org")
    assert "Student" not in out
    assert REDACTED in out


def test_redaction_leaves_the_rest_of_the_ticket_alone():
    out = redact(ACCESS_REQUEST, extract_email(ACCESS_REQUEST))
    assert "I need access to ds01 for working on my masters thesis." in out
    assert "### Type of request" in out


def test_redaction_of_no_address_is_a_no_op():
    assert redact(ACCESS_REQUEST, None) == ACCESS_REQUEST


def test_subject_carries_the_number_the_title_and_the_opener():
    assert compose_subject(28, "[QUESTION] VPN off campus", "someone") == (
        "[ds01-hub #28] [QUESTION] VPN off campus - someone"
    )


def test_the_subject_does_not_change_with_the_event():
    """It is the only thing holding a ticket's mails in one thread, so it is built from the
    ticket alone - nothing about opening, commenting or escalating may reach it."""
    assert compose_subject(28, "t", "someone") == compose_subject(28, "t", "someone")


def test_body_leads_with_the_url_and_closes_with_the_notice():
    out = compose_body("https://github.com/x/y/issues/28", ACCESS_REQUEST)
    assert out.splitlines()[0] == "https://github.com/x/y/issues/28"
    assert "### Type of request" in out
    assert out.rstrip().endswith("replies to this email are not tracked.")


def test_mask_keeps_one_character_of_the_local_part():
    assert mask("a.student@hertie-school.org") == "a***@hertie-school.org"


# ------------------------------------------------------------------------ HTML bodies


def test_the_html_body_leads_with_the_ticket_link():
    out = compose_html("https://github.com/o/r/issues/7", "<h3>Hertie email</h3>")
    assert (
        out.splitlines()[0]
        == '<p><a href="https://github.com/o/r/issues/7">https://github.com/o/r/issues/7</a></p>'
    )


def test_the_html_body_carries_githubs_rendering_verbatim():
    # GitHub sanitises; re-escaping its output here would show readers escaped tags.
    out = compose_html("https://x/1", "<h3>Heading</h3>\n<p>text</p>")
    assert "<h3>Heading</h3>" in out


def test_the_closing_line_survives_in_html():
    out = compose_html("https://x/1", "<p>x</p>")
    assert "Reply on the ticket" in out


def test_a_failed_render_returns_none_rather_than_raising(monkeypatch):
    # The caller falls back to plain text. A mail that reads like raw markdown is cosmetic;
    # a mail that never arrives is the actual fault.
    def boom(*_args, **_kwargs):
        raise OSError("no network")

    monkeypatch.setattr(notify_ticket.urllib.request, "urlopen", boom)
    assert render_markdown("### x", "o/r", "tok") is None


def test_a_rendered_body_is_sent_as_html(monkeypatch):
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command

        class R:
            returncode = 0

        return R()

    monkeypatch.setattr(notify_ticket.subprocess, "run", fake_run)
    assert send_mail("subj", "<p>b</p>", None, "ds01-hub-32", as_html=True) is True
    assert "--html" in captured["command"]


def test_a_plain_body_is_not_sent_as_html(monkeypatch):
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command

        class R:
            returncode = 0

        return R()

    monkeypatch.setattr(notify_ticket.subprocess, "run", fake_run)
    assert send_mail("subj", "plain", None, "ds01-hub-32") is True
    assert "--html" not in captured["command"]


def test_the_mail_carries_the_tickets_thread_key(monkeypatch):
    # Without this the mailer sends the old way and the ticket's mail splits into a thread
    # per event - which is the whole fault this flag exists to fix.
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command

        class R:
            returncode = 0

        return R()

    monkeypatch.setattr(notify_ticket.subprocess, "run", fake_run)
    assert send_mail("subj", "plain", "someone@hertie-school.org", "ds01-hub-32") is True
    command = captured["command"]
    assert command[command.index("--thread") + 1] == "ds01-hub-32"
    # The subject stays last, where the mailer's positional argument is.
    assert command[-1] == "subj"


# --------------------------------------------------------- recovering a redacted address


def _edits(*revisions):
    """A GraphQL reply carrying `(editedAt, body)` pairs, in the order given."""
    return {
        "data": {
            "repository": {
                "issue": {
                    "userContentEdits": {
                        "nodes": [{"editedAt": when, "diff": body} for when, body in revisions]
                    }
                }
            }
        }
    }


ORIGINAL = ACCESS_REQUEST
SCRUBBED = ACCESS_REQUEST.replace("a.student@students.hertie-school.org", REDACTED)


def test_the_first_revision_is_the_one_read(monkeypatch):
    # The newest revision is the redaction itself, and its address field says so.
    monkeypatch.setattr(
        notify_ticket,
        "github_api",
        lambda *_a, **_k: _edits(
            ("2026-09-17T11:54:24Z", SCRUBBED), ("2026-09-17T11:54:10Z", ORIGINAL)
        ),
    )
    assert extract_email(first_revision_body("o/r", 32, "tok")) == (
        "a.student@students.hertie-school.org"
    )


def test_a_ticket_that_was_never_edited_has_no_earlier_revision(monkeypatch):
    monkeypatch.setattr(notify_ticket, "github_api", lambda *_a, **_k: _edits())
    assert first_revision_body("o/r", 32, "tok") is None


def test_a_revision_without_a_readable_body_is_skipped(monkeypatch):
    # `diff` is null for a viewer without push access; the caller must mail the lab anyway.
    monkeypatch.setattr(
        notify_ticket, "github_api", lambda *_a, **_k: _edits(("2026-09-17T11:54:10Z", None))
    )
    assert first_revision_body("o/r", 32, "tok") is None


def test_a_failed_history_lookup_returns_none_rather_than_raising(monkeypatch):
    def boom(*_args, **_kwargs):
        raise OSError("no network")

    monkeypatch.setattr(notify_ticket, "github_api", boom)
    assert first_revision_body("o/r", 32, "tok") is None


def test_a_live_address_is_used_without_asking_for_history(monkeypatch):
    # A ticket whose redaction never ran still has the address in it, and a second request
    # would be wasted.
    def fail(*_args, **_kwargs):
        raise AssertionError("history must not be read when the body still has the address")

    monkeypatch.setattr(notify_ticket, "github_api", fail)
    assert opener_address("o/r", 32, ORIGINAL, "tok") == "a.student@students.hertie-school.org"


def test_a_redacted_body_falls_back_to_history(monkeypatch):
    monkeypatch.setattr(
        notify_ticket,
        "github_api",
        lambda *_a, **_k: _edits(("2026-09-17T11:54:10Z", ORIGINAL)),
    )
    assert opener_address("o/r", 32, SCRUBBED, "tok") == "a.student@students.hertie-school.org"


def test_an_unrecoverable_address_is_none_not_an_error(monkeypatch):
    monkeypatch.setattr(notify_ticket, "github_api", lambda *_a, **_k: _edits())
    assert opener_address("o/r", 32, SCRUBBED, "tok") is None


# ------------------------------------------------------------------------- new comments


def issue(number=32, body=SCRUBBED):
    return {
        "number": number,
        "title": "[QUESTION] VPN off campus",
        "body": body,
        "html_url": f"https://github.com/o/r/issues/{number}",
        "user": {"login": "drees"},
    }


def comment(login="henrycgbaker"):
    return {
        "body": "You need the DS01 route added to your VPN profile.",
        "html_url": "https://github.com/o/r/issues/32#issuecomment-1",
        "user": {"login": login},
    }


@pytest.fixture
def mailed(monkeypatch):
    """Captures the one mail a path sends, and the labels it deletes."""
    sent = {"deleted": []}

    def fake_mail(subject, url, text, cc, thread, _repo, _token, lead=""):
        sent.update(subject=subject, url=url, text=text, cc=cc, thread=thread, lead=lead)
        return sent.get("succeeds", True)

    def fake_api(method, url, *_a, **_k):
        if method == "DELETE":
            sent["deleted"].append(url.rsplit("/", 1)[-1])
            return None
        return _edits(("2026-09-17T11:54:10Z", ORIGINAL))

    monkeypatch.setattr(notify_ticket, "mail_rendered", fake_mail)
    monkeypatch.setattr(notify_ticket, "github_api", fake_api)
    return sent


def test_a_comment_mails_under_the_tickets_subject(mailed):
    notify_ticket.handle_comment(issue(), comment(), "o/r", "tok")
    assert mailed["subject"] == "[ds01-hub #32] [QUESTION] VPN off campus - drees"


def test_a_comment_mails_into_the_tickets_thread(mailed):
    notify_ticket.handle_comment(issue(), comment(), "o/r", "tok")
    assert mailed["thread"] == "ds01-hub-32"


def test_a_comment_copies_the_opener_recovered_from_history(mailed):
    notify_ticket.handle_comment(issue(), comment(), "o/r", "tok")
    assert mailed["cc"] == "a.student@students.hertie-school.org"


def test_a_comment_mail_links_the_comment_not_the_ticket(mailed):
    # The reader's next action is the thing that was just said.
    notify_ticket.handle_comment(issue(), comment(), "o/r", "tok")
    assert mailed["url"].endswith("#issuecomment-1")


def test_a_comment_mail_says_who_wrote_it(mailed):
    notify_ticket.handle_comment(issue(), comment("drees"), "o/r", "tok")
    assert mailed["lead"] == "New comment from drees"


def test_a_comment_resets_both_escalation_rungs(mailed):
    notify_ticket.handle_comment(issue(), comment(), "o/r", "tok")
    assert mailed["deleted"] == ["followed-up-48h", "followed-up-7d"]


def test_the_rungs_are_reset_even_when_the_mail_fails(mailed):
    # The clock measures when the ticket was last touched, which is a fact about the ticket
    # and not about our mail channel.
    mailed["succeeds"] = False
    assert notify_ticket.handle_comment(issue(), comment(), "o/r", "tok") == 1
    assert mailed["deleted"] == ["followed-up-48h", "followed-up-7d"]


def test_a_missing_rung_label_is_not_an_error(monkeypatch):
    # Most tickets never reach a rung, so a 404 is the ordinary case.
    def not_found(*_args, **_kwargs):
        raise notify_ticket.urllib.error.HTTPError("u", 404, "Not Found", {}, None)

    monkeypatch.setattr(notify_ticket, "github_api", not_found)
    notify_ticket.reset_followup_rungs("o/r", 32, "tok")


# ------------------------------------------------------------------------ manual resend


def test_a_backfill_mails_the_newest_comment(monkeypatch, mailed):
    def fake_api(method, url, *_a, **_k):
        if method == "DELETE":
            mailed["deleted"].append(url.rsplit("/", 1)[-1])
            return None
        if url.endswith("/issues/32"):
            return {**issue(), "comments": 3}
        return _edits(("2026-09-17T11:54:10Z", ORIGINAL))

    monkeypatch.setattr(notify_ticket, "github_api", fake_api)
    monkeypatch.setattr(notify_ticket, "newest_comment", lambda *_a, **_k: comment())
    assert notify_ticket.handle_backfill(32, "o/r", "tok") == 0
    assert mailed["subject"] == "[ds01-hub #32] [QUESTION] VPN off campus - drees"
    assert mailed["thread"] == "ds01-hub-32"


def test_a_backfill_of_a_ticket_with_no_comments_fails_loudly(monkeypatch, mailed):
    monkeypatch.setattr(notify_ticket, "github_api", lambda *_a, **_k: {**issue(), "comments": 0})
    monkeypatch.setattr(notify_ticket, "newest_comment", lambda *_a, **_k: None)
    assert notify_ticket.handle_backfill(32, "o/r", "tok") == 1
    assert "subject" not in mailed


# -------------------------------------------------------------- the lead line in a body


def test_a_lead_line_appears_above_the_rendered_text():
    out = compose_html("https://x/1", "<p>text</p>", "New comment from drees")
    assert "<strong>New comment from drees</strong>" in out
    assert out.index("New comment from drees") < out.index("<p>text</p>")


def test_a_lead_line_cannot_inject_html():
    out = compose_html("https://x/1", "<p>t</p>", "<script>x</script>")
    assert "<script>" not in out


def test_a_plain_body_carries_the_lead_too():
    out = compose_body("https://x/1", "text", "New comment from drees")
    assert "New comment from drees" in out
    assert out.splitlines()[0] == "https://x/1"


def test_an_opening_mail_has_no_lead_line():
    out = compose_html("https://x/1", "<p>t</p>")
    assert "<strong>" not in out
