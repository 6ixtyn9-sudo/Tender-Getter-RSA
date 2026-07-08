"""Tests for the National Digital Platform tender source plug-in."""
import pytest


def test_ndp_tenders_source_initialization():
    from tender_getter.sources.research_extra.ndp_tenders import NdpSource
    src = NdpSource()
    assert src.source_id == "ndp_tenders"
    assert src.live is False


def test_ndp_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ndp_tenders import NdpSource, MOCK_HTML
    src = NdpSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ndp_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ndp_tenders import NdpSource
    src = NdpSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
