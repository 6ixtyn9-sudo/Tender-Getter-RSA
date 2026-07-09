"""Tests for the eThekwini Water and Sanitation tender source plug-in."""
import pytest


def test_ethekwini_water_source_initialization():
    from tender_getter.sources.water.ethekwini_water import EthekwiniWaterSource
    src = EthekwiniWaterSource()
    assert src.source_id == "ethekwini_water"
    assert isinstance(src.live, bool)


def test_ethekwini_water_parse_mock_html():
    from tender_getter.sources.water.ethekwini_water import EthekwiniWaterSource, MOCK_HTML
    src = EthekwiniWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ethekwini_water_fetch_uses_fallback_on_empty():
    from tender_getter.sources.water.ethekwini_water import EthekwiniWaterSource
    src = EthekwiniWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
