"""Tests for the Western Cape Agriculture (Elsenburg) tender source plug-in."""
import pytest


def test_wc_agriculture_source_initialization():
    from tender_getter.sources.provincial.wc_agriculture import WcAgricultureSource
    src = WcAgricultureSource()
    assert src.source_id == "wc_agriculture"
    assert isinstance(src.live, bool)


def test_wc_agriculture_parse_mock_html():
    from tender_getter.sources.provincial.wc_agriculture import WcAgricultureSource, MOCK_HTML
    src = WcAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.provincial.wc_agriculture import WcAgricultureSource
    src = WcAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
