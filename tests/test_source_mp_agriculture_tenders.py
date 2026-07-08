"""Tests for the Mpumalanga Agriculture tender source plug-in."""
import pytest


def test_mp_agriculture_tenders_source_initialization():
    from tender_getter.sources.research_extra.mp_agriculture_tenders import MpAgricultureSource
    src = MpAgricultureSource()
    assert src.source_id == "mp_agriculture_tenders"
    assert src.live is False


def test_mp_agriculture_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mp_agriculture_tenders import MpAgricultureSource, MOCK_HTML
    src = MpAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_agriculture_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mp_agriculture_tenders import MpAgricultureSource
    src = MpAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
