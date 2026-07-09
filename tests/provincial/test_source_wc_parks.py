"""Tests for the CapeNature tender source plug-in."""
import pytest


def test_wc_parks_source_initialization():
    from tender_getter.sources.provincial.wc_parks import WcParksSource
    src = WcParksSource()
    assert src.source_id == "wc_parks"
    assert isinstance(src.live, bool)


def test_wc_parks_parse_mock_html():
    from tender_getter.sources.provincial.wc_parks import WcParksSource, MOCK_HTML
    src = WcParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_parks_fetch_uses_fallback_on_empty():
    from tender_getter.sources.provincial.wc_parks import WcParksSource
    src = WcParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
