"""Tests for the South African Human Rights Commission (SAHRC) tender source plug-in."""
import pytest


def test_sahrc_source_initialization():
    from tender_getter.sources.chapter9.sahrc import SahrcSource
    src = SahrcSource()
    assert src.source_id == "sahrc"
    assert isinstance(src.live, bool)


def test_sahrc_parse_mock_html():
    from tender_getter.sources.chapter9.sahrc import SahrcSource, MOCK_HTML
    src = SahrcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sahrc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.sahrc import SahrcSource
    src = SahrcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
