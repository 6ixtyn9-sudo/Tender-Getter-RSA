"""Tests for the University of South Africa (UNISA) tender source plug-in."""
import pytest


def test_unisa_tenders_source_initialization():
    from tender_getter.sources.universities.unisa_tenders import UnisaSource
    src = UnisaSource()
    assert src.source_id == "unisa_tenders"
    assert src.live is True


def test_unisa_tenders_parse_mock_html():
    from tender_getter.sources.universities.unisa_tenders import UnisaSource, MOCK_HTML
    src = UnisaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_unisa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.unisa_tenders import UnisaSource
    src = UnisaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
