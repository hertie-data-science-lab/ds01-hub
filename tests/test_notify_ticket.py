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

from notify_ticket import (
    REDACTED,
    compose_body,
    compose_subject,
    extract_email,
    field_value,
    mask,
    redact,
)

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


def test_subject_uses_the_first_label():
    assert compose_subject(28, ["resource-access-request"], "someone") == (
        "[ds01-hub #28] resource-access-request - someone"
    )


def test_subject_falls_back_when_the_ticket_has_no_labels():
    assert compose_subject(28, [], "someone") == "[ds01-hub #28] Issue - someone"


def test_body_leads_with_the_url_and_closes_with_the_notice():
    out = compose_body("https://github.com/x/y/issues/28", ACCESS_REQUEST)
    assert out.splitlines()[0] == "https://github.com/x/y/issues/28"
    assert "### Type of request" in out
    assert out.rstrip().endswith("replies to this email are not tracked.")


def test_mask_keeps_one_character_of_the_local_part():
    assert mask("a.student@hertie-school.org") == "a***@hertie-school.org"
