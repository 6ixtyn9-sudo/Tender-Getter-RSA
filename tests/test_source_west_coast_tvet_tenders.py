"""Tests for the West Coast TVET College tender source plug-in."""
import pytest


def test_west_coast_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.west_coast_tvet_tenders import WestCoastTvetSource
    src = WestCoastTvetSource()
    assert src.source_id == "west_coast_tvet_tenders"
    assert src.live is True


def test_west_coast_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.west_coast_tvet_tenders import WestCoastTvetSource, MOCK_HTML
    src = WestCoastTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_west_coast_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.west_coast_tvet_tenders import WestCoastTvetSource
    src = WestCoastTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
