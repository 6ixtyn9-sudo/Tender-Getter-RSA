"""Tests for the Mopani West TVET College tender source plug-in."""
import pytest


def test_mopani_west_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.mopani_west_tvet_tenders import MopaniWestTvetSource
    src = MopaniWestTvetSource()
    assert src.source_id == "mopani_west_tvet_tenders"
    assert src.live is True


def test_mopani_west_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.mopani_west_tvet_tenders import MopaniWestTvetSource, MOCK_HTML
    src = MopaniWestTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mopani_west_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.mopani_west_tvet_tenders import MopaniWestTvetSource
    src = MopaniWestTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
