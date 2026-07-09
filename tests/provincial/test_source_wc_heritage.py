"""Tests for the Western Cape Heritage tender source plug-in."""
import pytest


def test_wc_heritage_source_initialization():
    from tender_getter.sources.provincial.wc_heritage import WcHeritageSource
    src = WcHeritageSource()
    assert src.source_id == "wc_heritage"
    assert isinstance(src.live, bool)


def test_wc_heritage_parse_mock_html():
    from tender_getter.sources.provincial.wc_heritage import WcHeritageSource, MOCK_HTML
    src = WcHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_heritage_fetch_uses_fallback_on_empty():
    from tender_getter.sources.provincial.wc_heritage import WcHeritageSource
    src = WcHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
