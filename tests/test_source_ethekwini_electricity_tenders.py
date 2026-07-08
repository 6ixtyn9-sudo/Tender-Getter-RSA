"""Tests for the eThekwini Electricity tender source plug-in."""
import pytest


def test_ethekwini_electricity_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ethekwini_electricity_tenders import EthekwiniElectricitySource
    src = EthekwiniElectricitySource()
    assert src.source_id == "ethekwini_electricity_tenders"
    assert src.live is True


def test_ethekwini_electricity_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ethekwini_electricity_tenders import EthekwiniElectricitySource, MOCK_HTML
    src = EthekwiniElectricitySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ethekwini_electricity_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ethekwini_electricity_tenders import EthekwiniElectricitySource
    src = EthekwiniElectricitySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
