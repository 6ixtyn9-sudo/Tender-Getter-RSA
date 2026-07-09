"""Tests for the Wholesale and Retail Sector Education and Training Authority (W&RSETA) tender source plug-in."""
import pytest


def test_wrseta_source_initialization():
    from tender_getter.sources.setas.wrseta import WrsetaSource
    src = WrsetaSource()
    assert src.source_id == "wrseta"
    assert isinstance(src.live, bool)


def test_wrseta_parse_mock_html():
    from tender_getter.sources.setas.wrseta import WrsetaSource, MOCK_HTML
    src = WrsetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wrseta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.wrseta import WrsetaSource
    src = WrsetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
