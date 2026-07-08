"""Tests for the Limpopo Provincial Treasury tender source plug-in."""
import pytest


def test_limpopo_tenders_source_initialization():
    from tender_getter.sources.research_extra.limpopo_tenders import LimpopoSource
    src = LimpopoSource()
    assert src.source_id == "limpopo_tenders"
    assert src.live is True


def test_limpopo_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.limpopo_tenders import LimpopoSource, MOCK_HTML
    src = LimpopoSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_limpopo_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.limpopo_tenders import LimpopoSource
    src = LimpopoSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
