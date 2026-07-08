"""Tests for the Elias Motsoaledi (alt) tender source plug-in."""
import pytest


def test_elias_motsoaledi_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.elias_motsoaledi_alt_tenders import EliasMotsoalediAltSource
    src = EliasMotsoalediAltSource()
    assert src.source_id == "elias_motsoaledi_alt_tenders"
    assert src.live is False


def test_elias_motsoaledi_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.elias_motsoaledi_alt_tenders import EliasMotsoalediAltSource, MOCK_HTML
    src = EliasMotsoalediAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_elias_motsoaledi_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.elias_motsoaledi_alt_tenders import EliasMotsoalediAltSource
    src = EliasMotsoalediAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
