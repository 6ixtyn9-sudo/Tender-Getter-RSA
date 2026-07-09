"""Tests for the Mpumalanga Agriculture tender source plug-in."""
import pytest


def test_mp_agriculture_source_initialization():
    from tender_getter.sources.research.mp_agriculture import MpAgricultureSource
    src = MpAgricultureSource()
    assert src.source_id == "mp_agriculture"
    assert isinstance(src.live, bool)


def test_mp_agriculture_parse_mock_html():
    from tender_getter.sources.research.mp_agriculture import MpAgricultureSource, MOCK_HTML
    src = MpAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.mp_agriculture import MpAgricultureSource
    src = MpAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
