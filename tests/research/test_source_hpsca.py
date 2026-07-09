"""Tests for the Health Professions Council (alt) tender source plug-in."""
import pytest


def test_hpsca_source_initialization():
    from tender_getter.sources.research.hpsca import HpscaSource
    src = HpscaSource()
    assert src.source_id == "hpsca"
    assert src.live is False


def test_hpsca_parse_mock_html():
    from tender_getter.sources.research.hpsca import HpscaSource, MOCK_HTML
    src = HpscaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_hpsca_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.hpsca import HpscaSource
    src = HpscaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
