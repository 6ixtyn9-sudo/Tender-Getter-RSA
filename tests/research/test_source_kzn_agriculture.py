"""Tests for the KZN Agriculture and Rural Development tender source plug-in."""
import pytest


def test_kzn_agriculture_source_initialization():
    from tender_getter.sources.research.kzn_agriculture import KznAgricultureSource
    src = KznAgricultureSource()
    assert src.source_id == "kzn_agriculture"
    assert isinstance(src.live, bool)


def test_kzn_agriculture_parse_mock_html():
    from tender_getter.sources.research.kzn_agriculture import KznAgricultureSource, MOCK_HTML
    src = KznAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.kzn_agriculture import KznAgricultureSource
    src = KznAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
