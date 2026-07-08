"""Tests for the Free State Gambling and Liquor tender source plug-in."""
import pytest


def test_fs_liquor_tenders_source_initialization():
    from tender_getter.sources.research_extra.fs_liquor_tenders import FsLiquorSource
    src = FsLiquorSource()
    assert src.source_id == "fs_liquor_tenders"
    assert src.live is False


def test_fs_liquor_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.fs_liquor_tenders import FsLiquorSource, MOCK_HTML
    src = FsLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_liquor_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.fs_liquor_tenders import FsLiquorSource
    src = FsLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
