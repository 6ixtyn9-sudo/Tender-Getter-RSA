"""Tests for the Port St Johns Local Municipality tender source plug-in."""
import pytest


def test_port_st_johns_lm_source_initialization():
    from tender_getter.sources.local_municipalities.port_st_johns_lm import PortStJohnsLmSource
    src = PortStJohnsLmSource()
    assert src.source_id == "port_st_johns_lm"
    assert src.live is True


def test_port_st_johns_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.port_st_johns_lm import PortStJohnsLmSource, MOCK_HTML
    src = PortStJohnsLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_port_st_johns_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.port_st_johns_lm import PortStJohnsLmSource
    src = PortStJohnsLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
