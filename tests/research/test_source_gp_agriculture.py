"""Tests for the Gauteng Agriculture and Rural Development tender source plug-in."""
import pytest


def test_gp_agriculture_source_initialization():
    from tender_getter.sources.research.gp_agriculture import GpAgricultureSource
    src = GpAgricultureSource()
    assert src.source_id == "gp_agriculture"
    assert isinstance(src.live, bool)


def test_gp_agriculture_parse_mock_html():
    from tender_getter.sources.research.gp_agriculture import GpAgricultureSource, MOCK_HTML
    src = GpAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gp_agriculture import GpAgricultureSource
    src = GpAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
