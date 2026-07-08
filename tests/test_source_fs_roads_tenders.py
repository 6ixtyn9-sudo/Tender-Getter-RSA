"""Tests for the Free State Roads tender source plug-in."""
import pytest


def test_fs_roads_tenders_source_initialization():
    from tender_getter.sources.research_extra.fs_roads_tenders import FsRoadsSource
    src = FsRoadsSource()
    assert src.source_id == "fs_roads_tenders"
    assert src.live is False


def test_fs_roads_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.fs_roads_tenders import FsRoadsSource, MOCK_HTML
    src = FsRoadsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_roads_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.fs_roads_tenders import FsRoadsSource
    src = FsRoadsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
