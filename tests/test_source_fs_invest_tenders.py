"""Tests for the Free State Investment tender source plug-in."""
import pytest


def test_fs_invest_tenders_source_initialization():
    from tender_getter.sources.research_extra.fs_invest_tenders import FsInvestSource
    src = FsInvestSource()
    assert src.source_id == "fs_invest_tenders"
    assert src.live is False


def test_fs_invest_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.fs_invest_tenders import FsInvestSource, MOCK_HTML
    src = FsInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_invest_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.fs_invest_tenders import FsInvestSource
    src = FsInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
