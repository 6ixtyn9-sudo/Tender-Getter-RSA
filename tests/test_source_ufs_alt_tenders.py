"""Tests for the UFS (alt) tender source plug-in."""
import pytest


def test_ufs_alt_tenders_source_initialization():
    from tender_getter.sources.universities.ufs_alt_tenders import UfsAltSource
    src = UfsAltSource()
    assert src.source_id == "ufs_alt_tenders"
    assert src.live is True


def test_ufs_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.ufs_alt_tenders import UfsAltSource, MOCK_HTML
    src = UfsAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ufs_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.ufs_alt_tenders import UfsAltSource
    src = UfsAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
