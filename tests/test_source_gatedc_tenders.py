"""Tests for the Gauteng Enterprise Propeller / TIK tender source plug-in."""
import pytest


def test_gatedc_tenders_source_initialization():
    from tender_getter.sources.research_extra.gatedc_tenders import GatedcSource
    src = GatedcSource()
    assert src.source_id == "gatedc_tenders"
    assert src.live is False


def test_gatedc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gatedc_tenders import GatedcSource, MOCK_HTML
    src = GatedcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gatedc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gatedc_tenders import GatedcSource
    src = GatedcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
