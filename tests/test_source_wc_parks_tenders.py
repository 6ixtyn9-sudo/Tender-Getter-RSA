"""Tests for the CapeNature tender source plug-in."""
import pytest


def test_wc_parks_tenders_source_initialization():
    from tender_getter.sources.research_extra.wc_parks_tenders import WcParksSource
    src = WcParksSource()
    assert src.source_id == "wc_parks_tenders"
    assert src.live is True


def test_wc_parks_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wc_parks_tenders import WcParksSource, MOCK_HTML
    src = WcParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_parks_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wc_parks_tenders import WcParksSource
    src = WcParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
