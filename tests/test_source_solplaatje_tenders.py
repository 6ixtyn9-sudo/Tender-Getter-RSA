"""Tests for the Sol Plaatje University tender source plug-in."""
import pytest


def test_solplaatje_tenders_source_initialization():
    from tender_getter.sources.universities.solplaatje_tenders import SolplaatjeSource
    src = SolplaatjeSource()
    assert src.source_id == "solplaatje_tenders"
    assert src.live is True


def test_solplaatje_tenders_parse_mock_html():
    from tender_getter.sources.universities.solplaatje_tenders import SolplaatjeSource, MOCK_HTML
    src = SolplaatjeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_solplaatje_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.solplaatje_tenders import SolplaatjeSource
    src = SolplaatjeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
