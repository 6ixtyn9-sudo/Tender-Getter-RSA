"""Tests for the Free State Heritage tender source plug-in."""
import pytest


def test_fs_heritage_source_initialization():
    from tender_getter.sources.research.fs_heritage import FsHeritageSource
    src = FsHeritageSource()
    assert src.source_id == "fs_heritage"
    assert src.live is False


def test_fs_heritage_parse_mock_html():
    from tender_getter.sources.research.fs_heritage import FsHeritageSource, MOCK_HTML
    src = FsHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_heritage_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fs_heritage import FsHeritageSource
    src = FsHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
