"""Tests for the University of the Free State tender source plug-in."""
import pytest


def test_ufs_tenders_source_initialization():
    from tender_getter.sources.universities.ufs_tenders import UfsSource
    src = UfsSource()
    assert src.source_id == "ufs_tenders"
    assert src.live is True


def test_ufs_tenders_parse_mock_html():
    from tender_getter.sources.universities.ufs_tenders import UfsSource, MOCK_HTML
    src = UfsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ufs_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.ufs_tenders import UfsSource
    src = UfsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
