"""Tests for the Mpumalanga Health tender source plug-in."""
import pytest


def test_mp_health_tenders_source_initialization():
    from tender_getter.sources.research_extra.mp_health_tenders import MpHealthSource
    src = MpHealthSource()
    assert src.source_id == "mp_health_tenders"
    assert src.live is True


def test_mp_health_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mp_health_tenders import MpHealthSource, MOCK_HTML
    src = MpHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_health_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mp_health_tenders import MpHealthSource
    src = MpHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
