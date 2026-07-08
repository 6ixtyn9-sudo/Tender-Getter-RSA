"""Tests for the Mpumalanga Housing Board tender source plug-in."""
import pytest


def test_mp_housing_tenders_source_initialization():
    from tender_getter.sources.research_extra.mp_housing_tenders import MpHousingSource
    src = MpHousingSource()
    assert src.source_id == "mp_housing_tenders"
    assert src.live is False


def test_mp_housing_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mp_housing_tenders import MpHousingSource, MOCK_HTML
    src = MpHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_housing_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mp_housing_tenders import MpHousingSource
    src = MpHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
