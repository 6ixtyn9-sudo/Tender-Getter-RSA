"""Tests for the Limpopo Economic Development Agency (LEDA) tender source plug-in."""
import pytest


def test_lp_dev_source_initialization():
    from tender_getter.sources.research.lp_dev import LpDevSource
    src = LpDevSource()
    assert src.source_id == "lp_dev"
    assert src.live is False


def test_lp_dev_parse_mock_html():
    from tender_getter.sources.research.lp_dev import LpDevSource, MOCK_HTML
    src = LpDevSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_dev_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.lp_dev import LpDevSource
    src = LpDevSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
