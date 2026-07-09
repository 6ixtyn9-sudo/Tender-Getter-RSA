"""Tests for the University of KwaZulu-Natal tender source plug-in."""
import pytest


def test_ukzn_source_initialization():
    from tender_getter.sources.universities.ukzn import UkznSource
    src = UkznSource()
    assert src.source_id == "ukzn"
    assert isinstance(src.live, bool)


def test_ukzn_parse_mock_html():
    from tender_getter.sources.universities.ukzn import UkznSource, MOCK_HTML
    src = UkznSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ukzn_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.ukzn import UkznSource
    src = UkznSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
