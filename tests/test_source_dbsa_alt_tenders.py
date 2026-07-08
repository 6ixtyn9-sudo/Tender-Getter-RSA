"""Tests for the DBSA (alt) tender source plug-in."""
import pytest


def test_dbsa_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dbsa_alt_tenders import DbsaAltSource
    src = DbsaAltSource()
    assert src.source_id == "dbsa_alt_tenders"
    assert src.live is True


def test_dbsa_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dbsa_alt_tenders import DbsaAltSource, MOCK_HTML
    src = DbsaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dbsa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dbsa_alt_tenders import DbsaAltSource
    src = DbsaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
