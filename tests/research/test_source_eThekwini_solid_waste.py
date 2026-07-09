"""Tests for the eThekwini Solid Waste Unit tender source plug-in."""
import pytest


def test_eThekwini_solid_waste_source_initialization():
    from tender_getter.sources.research.eThekwini_solid_waste import EthekwiniSolidWasteSource
    src = EthekwiniSolidWasteSource()
    assert src.source_id == "eThekwini_solid_waste"
    assert isinstance(src.live, bool)


def test_eThekwini_solid_waste_parse_mock_html():
    from tender_getter.sources.research.eThekwini_solid_waste import EthekwiniSolidWasteSource, MOCK_HTML
    src = EthekwiniSolidWasteSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eThekwini_solid_waste_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.eThekwini_solid_waste import EthekwiniSolidWasteSource
    src = EthekwiniSolidWasteSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
