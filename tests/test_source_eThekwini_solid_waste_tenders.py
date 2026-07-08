"""Tests for the eThekwini Solid Waste Unit tender source plug-in."""
import pytest


def test_eThekwini_solid_waste_tenders_source_initialization():
    from tender_getter.sources.research_extra.eThekwini_solid_waste_tenders import EthekwiniSolidWasteSource
    src = EthekwiniSolidWasteSource()
    assert src.source_id == "eThekwini_solid_waste_tenders"
    assert src.live is True


def test_eThekwini_solid_waste_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.eThekwini_solid_waste_tenders import EthekwiniSolidWasteSource, MOCK_HTML
    src = EthekwiniSolidWasteSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eThekwini_solid_waste_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.eThekwini_solid_waste_tenders import EthekwiniSolidWasteSource
    src = EthekwiniSolidWasteSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
