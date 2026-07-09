"""Tests for the College of Cape Town TVET tender source plug-in."""
import pytest


def test_cape_town_tvet_source_initialization():
    from tender_getter.sources.tvet.cape_town_tvet import CapeTownTvetSource
    src = CapeTownTvetSource()
    assert src.source_id == "cape_town_tvet"
    assert isinstance(src.live, bool)


def test_cape_town_tvet_parse_mock_html():
    from tender_getter.sources.tvet.cape_town_tvet import CapeTownTvetSource, MOCK_HTML
    src = CapeTownTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cape_town_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.cape_town_tvet import CapeTownTvetSource
    src = CapeTownTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
