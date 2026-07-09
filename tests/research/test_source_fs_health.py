"""Tests for the Free State Health tender source plug-in."""
import pytest


def test_fs_health_source_initialization():
    from tender_getter.sources.research.fs_health import FsHealthSource
    src = FsHealthSource()
    assert src.source_id == "fs_health"
    assert isinstance(src.live, bool)


def test_fs_health_parse_mock_html():
    from tender_getter.sources.research.fs_health import FsHealthSource, MOCK_HTML
    src = FsHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_health_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fs_health import FsHealthSource
    src = FsHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
