"""Tests for the Free State Roads tender source plug-in."""
import pytest


def test_fs_roads_source_initialization():
    from tender_getter.sources.research.fs_roads import FsRoadsSource
    src = FsRoadsSource()
    assert src.source_id == "fs_roads"
    assert isinstance(src.live, bool)


def test_fs_roads_parse_mock_html():
    from tender_getter.sources.research.fs_roads import FsRoadsSource, MOCK_HTML
    src = FsRoadsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_roads_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fs_roads import FsRoadsSource
    src = FsRoadsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
