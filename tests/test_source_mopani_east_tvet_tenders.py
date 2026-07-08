"""Tests for the Mopani East TVET College tender source plug-in."""
import pytest


def test_mopani_east_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.mopani_east_tvet_tenders import MopaniEastTvetSource
    src = MopaniEastTvetSource()
    assert src.source_id == "mopani_east_tvet_tenders"
    assert src.live is True


def test_mopani_east_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.mopani_east_tvet_tenders import MopaniEastTvetSource, MOCK_HTML
    src = MopaniEastTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mopani_east_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.mopani_east_tvet_tenders import MopaniEastTvetSource
    src = MopaniEastTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
