"""Tests for the Sol Plaatje (alt) tender source plug-in."""
import pytest


def test_solplaatje_alt_tenders_source_initialization():
    from tender_getter.sources.universities.solplaatje_alt_tenders import SolplaatjeAltSource
    src = SolplaatjeAltSource()
    assert src.source_id == "solplaatje_alt_tenders"
    assert src.live is True


def test_solplaatje_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.solplaatje_alt_tenders import SolplaatjeAltSource, MOCK_HTML
    src = SolplaatjeAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_solplaatje_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.solplaatje_alt_tenders import SolplaatjeAltSource
    src = SolplaatjeAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
