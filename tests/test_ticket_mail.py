"""Tests for the pieces both ticket mailers share.

`compose_subject` is exercised through its callers; what is asserted here is the one piece
of GitHub trivia that moved in with it. `newest_comment` reaches for the last page of a
one-per-page listing to avoid paging a ticket's whole history, which is the kind of trick
that is quietly broken by a well-meaning edit.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

import ticket_mail
from ticket_mail import compose_subject, compose_thread_key, newest_comment


def test_a_ticket_with_no_comments_costs_no_request(monkeypatch):
    def fail(*_args, **_kwargs):
        raise AssertionError("a ticket with no comments must not cost a request")

    monkeypatch.setattr(ticket_mail, "github_api", fail)
    assert newest_comment("o/r", 32, 0, "tok") is None


def test_the_last_page_of_a_one_per_page_listing_is_asked_for(monkeypatch):
    seen = {}

    def capture(_method, url, *_a, **_k):
        seen["url"] = url
        return [{"id": 7}]

    monkeypatch.setattr(ticket_mail, "github_api", capture)
    assert newest_comment("o/r", 32, 7, "tok") == {"id": 7}
    assert "per_page=1" in seen["url"]
    assert "page=7" in seen["url"]
    assert "/repos/o/r/issues/32/comments?" in seen["url"]


def test_an_empty_page_is_no_comment_rather_than_an_error(monkeypatch):
    # A comment deleted between reading the count and reading the page.
    monkeypatch.setattr(ticket_mail, "github_api", lambda *_a, **_k: [])
    assert newest_comment("o/r", 32, 3, "tok") is None


@pytest.mark.parametrize("title", ["a ticket", "", "with - dashes - in it"])
def test_the_subject_is_built_from_the_ticket_alone(title):
    # Nothing about the event may reach it, or the mail starts its own thread.
    assert compose_subject(4, title, "someone") == f"[ds01-hub #4] {title} - someone"


def test_the_thread_key_is_the_number_and_nothing_else():
    # The complement of the test above. A ticket renamed after its opening mail gets a new
    # SUBJECT, which is what splits a subject-keyed thread; the key must not move with it.
    assert compose_thread_key(4) == "ds01-hub-4"
    assert compose_subject(4, "renamed", "someone") != compose_subject(4, "a ticket", "someone")


def test_two_tickets_are_two_threads():
    assert compose_thread_key(4) != compose_thread_key(5)


def test_the_thread_key_is_a_plain_token_the_mailer_will_accept():
    # The mailer refuses anything else and sends unthreaded instead - see its _THREAD_KEY_RE.
    assert re.fullmatch(r"[A-Za-z0-9._-]{1,64}", compose_thread_key(12345))
