"""Tests for the Capricorn District Municipality tender source plug-in."""
import pytest


def test_capricorn_tenders_source_initialization():
    from tender_getter.sources.research_extra.capricorn_tenders import CapricornSource
    src = CapricornSource()
    assert src.source_id == "capricorn_tenders"
    assert src.live is True


def test_capricorn_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.capricorn_tenders import CapricornSource, MOCK_HTML
    src = CapricornSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_capricorn_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.capricorn_tenders import CapricornSource
    src = CapricornSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
