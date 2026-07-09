"""Tests for the Bohlabela District Municipality tender source plug-in."""
import pytest


def test_bohlabela_dm_source_initialization():
    from tender_getter.sources.districts.bohlabela_dm import BohlabelaDmSource
    src = BohlabelaDmSource()
    assert src.source_id == "bohlabela_dm"
    assert src.live is False


def test_bohlabela_dm_parse_mock_html():
    from tender_getter.sources.districts.bohlabela_dm import BohlabelaDmSource, MOCK_HTML
    src = BohlabelaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_bohlabela_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.bohlabela_dm import BohlabelaDmSource
    src = BohlabelaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
