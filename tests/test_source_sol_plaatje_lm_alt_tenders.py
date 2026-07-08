"""Tests for the Sol Plaatje (alt) tender source plug-in."""
import pytest


def test_sol_plaatje_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.sol_plaatje_lm_alt_tenders import SolPlaatjeLmAltSource
    src = SolPlaatjeLmAltSource()
    assert src.source_id == "sol_plaatje_lm_alt_tenders"
    assert src.live is True


def test_sol_plaatje_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.sol_plaatje_lm_alt_tenders import SolPlaatjeLmAltSource, MOCK_HTML
    src = SolPlaatjeLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sol_plaatje_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.sol_plaatje_lm_alt_tenders import SolPlaatjeLmAltSource
    src = SolPlaatjeLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
