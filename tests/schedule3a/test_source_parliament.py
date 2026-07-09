"""Tests for the Parliament of South Africa tender source plug-in."""
import pytest


def test_parliament_source_initialization():
    from tender_getter.sources.schedule3a.parliament import ParliamentSource
    src = ParliamentSource()
    assert src.source_id == "parliament"
    assert src.live is True


def test_parliament_parse_mock_html():
    from tender_getter.sources.schedule3a.parliament import ParliamentSource, MOCK_HTML
    src = ParliamentSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_parliament_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.parliament import ParliamentSource
    src = ParliamentSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
