"""Tests for the University of Johannesburg tender source plug-in."""
import pytest


def test_uj_source_initialization():
    from tender_getter.sources.universities.uj import UjSource
    src = UjSource()
    assert src.source_id == "uj"
    assert isinstance(src.live, bool)


def test_uj_parse_mock_html():
    from tender_getter.sources.universities.uj import UjSource, MOCK_HTML
    src = UjSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uj_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.uj import UjSource
    src = UjSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
