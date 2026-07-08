"""Tests for the National Skills Development Programme tender source plug-in."""
import pytest


def test_nsdp_tenders_source_initialization():
    from tender_getter.sources.research_extra.nsdp_tenders import NsdpSource
    src = NsdpSource()
    assert src.source_id == "nsdp_tenders"
    assert src.live is False


def test_nsdp_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nsdp_tenders import NsdpSource, MOCK_HTML
    src = NsdpSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nsdp_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nsdp_tenders import NsdpSource
    src = NsdpSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
