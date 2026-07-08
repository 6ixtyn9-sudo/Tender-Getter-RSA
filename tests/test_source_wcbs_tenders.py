"""Tests for the Western Cape Blood Service (WCBS) tender source plug-in."""
import pytest


def test_wcbs_tenders_source_initialization():
    from tender_getter.sources.research_extra.wcbs_tenders import WcbsSource
    src = WcbsSource()
    assert src.source_id == "wcbs_tenders"
    assert src.live is True


def test_wcbs_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wcbs_tenders import WcbsSource, MOCK_HTML
    src = WcbsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wcbs_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wcbs_tenders import WcbsSource
    src = WcbsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
