"""Tests for the Western Cape Blood Service (WCBS) tender source plug-in."""
import pytest


def test_wcbs_source_initialization():
    from tender_getter.sources.research.wcbs import WcbsSource
    src = WcbsSource()
    assert src.source_id == "wcbs"
    assert isinstance(src.live, bool)


def test_wcbs_parse_mock_html():
    from tender_getter.sources.research.wcbs import WcbsSource, MOCK_HTML
    src = WcbsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wcbs_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.wcbs import WcbsSource
    src = WcbsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
