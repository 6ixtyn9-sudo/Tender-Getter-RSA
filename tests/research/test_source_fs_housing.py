"""Tests for the Free State Housing tender source plug-in."""
import pytest


def test_fs_housing_source_initialization():
    from tender_getter.sources.research.fs_housing import FsHousingSource
    src = FsHousingSource()
    assert src.source_id == "fs_housing"
    assert src.live is False


def test_fs_housing_parse_mock_html():
    from tender_getter.sources.research.fs_housing import FsHousingSource, MOCK_HTML
    src = FsHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_housing_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fs_housing import FsHousingSource
    src = FsHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
