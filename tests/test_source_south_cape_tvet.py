"""Tests for the South Cape TVET College tender source plug-in."""
import pytest


def test_south_cape_tvet_source_initialization():
    from tender_getter.sources.tvet.south_cape_tvet import SouthCapeTvetSource
    src = SouthCapeTvetSource()
    assert src.source_id == "south_cape_tvet"
    assert src.live is True


def test_south_cape_tvet_parse_mock_html():
    from tender_getter.sources.tvet.south_cape_tvet import SouthCapeTvetSource, MOCK_HTML
    src = SouthCapeTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_south_cape_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.south_cape_tvet import SouthCapeTvetSource
    src = SouthCapeTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
