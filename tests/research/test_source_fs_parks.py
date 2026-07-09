"""Tests for the Free State Parks tender source plug-in."""
import pytest


def test_fs_parks_source_initialization():
    from tender_getter.sources.research.fs_parks import FsParksSource
    src = FsParksSource()
    assert src.source_id == "fs_parks"
    assert isinstance(src.live, bool)


def test_fs_parks_parse_mock_html():
    from tender_getter.sources.research.fs_parks import FsParksSource, MOCK_HTML
    src = FsParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_parks_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fs_parks import FsParksSource
    src = FsParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
