"""Tests for the Durban University of Technology tender source plug-in."""
import pytest


def test_dut_source_initialization():
    from tender_getter.sources.universities.dut import DutSource
    src = DutSource()
    assert src.source_id == "dut"
    assert isinstance(src.live, bool)


def test_dut_parse_mock_html():
    from tender_getter.sources.universities.dut import DutSource, MOCK_HTML
    src = DutSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dut_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.dut import DutSource
    src = DutSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
