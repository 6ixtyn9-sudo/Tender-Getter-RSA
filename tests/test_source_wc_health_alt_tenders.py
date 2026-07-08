"""Tests for the Western Cape Health (alt URL) tender source plug-in."""
import pytest


def test_wc_health_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.wc_health_alt_tenders import WcHealthAltSource
    src = WcHealthAltSource()
    assert src.source_id == "wc_health_alt_tenders"
    assert src.live is True


def test_wc_health_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.wc_health_alt_tenders import WcHealthAltSource, MOCK_HTML
    src = WcHealthAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_health_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.wc_health_alt_tenders import WcHealthAltSource
    src = WcHealthAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
