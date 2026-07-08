"""Tests for the Mpumalanga Tourism Authority tender source plug-in."""
import pytest


def test_mp_tourism_tenders_source_initialization():
    from tender_getter.sources.research_extra.mp_tourism_tenders import MpTourismSource
    src = MpTourismSource()
    assert src.source_id == "mp_tourism_tenders"
    assert src.live is False


def test_mp_tourism_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mp_tourism_tenders import MpTourismSource, MOCK_HTML
    src = MpTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_tourism_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mp_tourism_tenders import MpTourismSource
    src = MpTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
