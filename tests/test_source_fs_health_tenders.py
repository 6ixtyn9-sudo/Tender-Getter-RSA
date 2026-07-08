"""Tests for the Free State Health tender source plug-in."""
import pytest


def test_fs_health_tenders_source_initialization():
    from tender_getter.sources.research_extra.fs_health_tenders import FsHealthSource
    src = FsHealthSource()
    assert src.source_id == "fs_health_tenders"
    assert src.live is True


def test_fs_health_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.fs_health_tenders import FsHealthSource, MOCK_HTML
    src = FsHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_health_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.fs_health_tenders import FsHealthSource
    src = FsHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
