"""Tests for the Gauteng Enterprise Propeller / TIK tender source plug-in."""
import pytest


def test_gatedc_source_initialization():
    from tender_getter.sources.research.gatedc import GatedcSource
    src = GatedcSource()
    assert src.source_id == "gatedc"
    assert isinstance(src.live, bool)


def test_gatedc_parse_mock_html():
    from tender_getter.sources.research.gatedc import GatedcSource, MOCK_HTML
    src = GatedcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gatedc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gatedc import GatedcSource
    src = GatedcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
