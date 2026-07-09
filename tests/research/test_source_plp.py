"""Tests for the Provincial Licensing Practitioners tender source plug-in."""
import pytest


def test_plp_source_initialization():
    from tender_getter.sources.research.plp import PlpSource
    src = PlpSource()
    assert src.source_id == "plp"
    assert isinstance(src.live, bool)


def test_plp_parse_mock_html():
    from tender_getter.sources.research.plp import PlpSource, MOCK_HTML
    src = PlpSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_plp_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.plp import PlpSource
    src = PlpSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
