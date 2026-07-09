"""Tests for the Sol Plaatje University tender source plug-in."""
import pytest


def test_solplaatje_source_initialization():
    from tender_getter.sources.universities.solplaatje import SolplaatjeSource
    src = SolplaatjeSource()
    assert src.source_id == "solplaatje"
    assert isinstance(src.live, bool)


def test_solplaatje_parse_mock_html():
    from tender_getter.sources.universities.solplaatje import SolplaatjeSource, MOCK_HTML
    src = SolplaatjeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_solplaatje_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.solplaatje import SolplaatjeSource
    src = SolplaatjeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
