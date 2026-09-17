"""Tests for the pieces both ticket mailers share.

`compose_subject` is exercised through its callers; what is asserted here is the one piece
of GitHub trivia that moved in with it. `newest_comment` reaches for the last page of a
one-per-page listing to avoid paging a ticket's whole history, which is the kind of trick
that is quietly broken by a well-meaning edit.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

import ticket_mail
from ticket_mail import compose_subject, newest_comment


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
