"""Tests for the Western Cape Department of Health & Wellness tender source plug-in."""
import pytest


def test_wc_health_tenders_source_initialization():
    from tender_getter.sources.research_extra.wc_health_tenders import WcHealthSource
    src = WcHealthSource()
    assert src.source_id == "wc_health_tenders"
    assert src.live is True


def test_wc_health_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wc_health_tenders import WcHealthSource, MOCK_HTML
    src = WcHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_health_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wc_health_tenders import WcHealthSource
    src = WcHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
