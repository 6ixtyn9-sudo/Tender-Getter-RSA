"""Tests for the Western Cape Development Corporation (Wesgro) tender source plug-in."""
import pytest


def test_wc_dev_tenders_source_initialization():
    from tender_getter.sources.research_extra.wc_dev_tenders import WcDevSource
    src = WcDevSource()
    assert src.source_id == "wc_dev_tenders"
    assert src.live is False


def test_wc_dev_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wc_dev_tenders import WcDevSource, MOCK_HTML
    src = WcDevSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_dev_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wc_dev_tenders import WcDevSource
    src = WcDevSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
