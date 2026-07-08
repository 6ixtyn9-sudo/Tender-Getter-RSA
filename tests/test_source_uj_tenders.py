"""Tests for the University of Johannesburg tender source plug-in."""
import pytest


def test_uj_tenders_source_initialization():
    from tender_getter.sources.universities.uj_tenders import UjSource
    src = UjSource()
    assert src.source_id == "uj_tenders"
    assert src.live is True


def test_uj_tenders_parse_mock_html():
    from tender_getter.sources.universities.uj_tenders import UjSource, MOCK_HTML
    src = UjSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uj_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.uj_tenders import UjSource
    src = UjSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
