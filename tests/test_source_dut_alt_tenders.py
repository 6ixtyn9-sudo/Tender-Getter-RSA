"""Tests for the DUT (alt) tender source plug-in."""
import pytest


def test_dut_alt_tenders_source_initialization():
    from tender_getter.sources.universities.dut_alt_tenders import DutAltSource
    src = DutAltSource()
    assert src.source_id == "dut_alt_tenders"
    assert src.live is True


def test_dut_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.dut_alt_tenders import DutAltSource, MOCK_HTML
    src = DutAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dut_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.dut_alt_tenders import DutAltSource
    src = DutAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
