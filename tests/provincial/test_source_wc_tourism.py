"""Tests for the Western Cape Tourism tender source plug-in."""
import pytest


def test_wc_tourism_source_initialization():
    from tender_getter.sources.provincial.wc_tourism import WcTourismSource
    src = WcTourismSource()
    assert src.source_id == "wc_tourism"
    assert isinstance(src.live, bool)


def test_wc_tourism_parse_mock_html():
    from tender_getter.sources.provincial.wc_tourism import WcTourismSource, MOCK_HTML
    src = WcTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_tourism_fetch_uses_fallback_on_empty():
    from tender_getter.sources.provincial.wc_tourism import WcTourismSource
    src = WcTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
