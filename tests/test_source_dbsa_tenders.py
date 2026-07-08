"""Tests for the Development Bank of Southern Africa tender source plug-in."""
import pytest


def test_dbsa_tenders_source_initialization():
    from tender_getter.sources.research_extra.dbsa_tenders import DbsaSource
    src = DbsaSource()
    assert src.source_id == "dbsa_tenders"
    assert src.live is True


def test_dbsa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dbsa_tenders import DbsaSource, MOCK_HTML
    src = DbsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dbsa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dbsa_tenders import DbsaSource
    src = DbsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
