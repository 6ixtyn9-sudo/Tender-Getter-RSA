"""Tests for the Western Cape Heritage tender source plug-in."""
import pytest


def test_wc_heritage_tenders_source_initialization():
    from tender_getter.sources.research_extra.wc_heritage_tenders import WcHeritageSource
    src = WcHeritageSource()
    assert src.source_id == "wc_heritage_tenders"
    assert src.live is False


def test_wc_heritage_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wc_heritage_tenders import WcHeritageSource, MOCK_HTML
    src = WcHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_heritage_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wc_heritage_tenders import WcHeritageSource
    src = WcHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
