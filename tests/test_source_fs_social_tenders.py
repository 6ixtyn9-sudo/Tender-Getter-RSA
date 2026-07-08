"""Tests for the Free State Social Development tender source plug-in."""
import pytest


def test_fs_social_tenders_source_initialization():
    from tender_getter.sources.research_extra.fs_social_tenders import FsSocialSource
    src = FsSocialSource()
    assert src.source_id == "fs_social_tenders"
    assert src.live is False


def test_fs_social_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.fs_social_tenders import FsSocialSource, MOCK_HTML
    src = FsSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_social_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.fs_social_tenders import FsSocialSource
    src = FsSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
