"""Tests for the Port St Johns (alt) tender source plug-in."""
import pytest


def test_port_st_johns_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.port_st_johns_lm_alt_tenders import PortStJohnsLmAltSource
    src = PortStJohnsLmAltSource()
    assert src.source_id == "port_st_johns_lm_alt_tenders"
    assert src.live is False


def test_port_st_johns_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.port_st_johns_lm_alt_tenders import PortStJohnsLmAltSource, MOCK_HTML
    src = PortStJohnsLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_port_st_johns_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.port_st_johns_lm_alt_tenders import PortStJohnsLmAltSource
    src = PortStJohnsLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
