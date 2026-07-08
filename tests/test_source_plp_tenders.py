"""Tests for the Provincial Licensing Practitioners tender source plug-in."""
import pytest


def test_plp_tenders_source_initialization():
    from tender_getter.sources.research_extra.plp_tenders import PlpSource
    src = PlpSource()
    assert src.source_id == "plp_tenders"
    assert src.live is False


def test_plp_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.plp_tenders import PlpSource, MOCK_HTML
    src = PlpSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_plp_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.plp_tenders import PlpSource
    src = PlpSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
