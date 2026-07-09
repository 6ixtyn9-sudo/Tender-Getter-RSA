"""Tests for the Free State Agriculture tender source plug-in."""
import pytest


def test_fs_agriculture_source_initialization():
    from tender_getter.sources.research.fs_agriculture import FsAgricultureSource
    src = FsAgricultureSource()
    assert src.source_id == "fs_agriculture"
    assert src.live is False


def test_fs_agriculture_parse_mock_html():
    from tender_getter.sources.research.fs_agriculture import FsAgricultureSource, MOCK_HTML
    src = FsAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fs_agriculture import FsAgricultureSource
    src = FsAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
