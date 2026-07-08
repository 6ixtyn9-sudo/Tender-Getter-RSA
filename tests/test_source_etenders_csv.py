"""Tests for the National Treasury eTenders Bulk CSV tender source plug-in."""
import pytest


def test_etenders_csv_source_initialization():
    from tender_getter.sources.research_extra.etenders_csv import EtendersCsvSource
    src = EtendersCsvSource()
    assert src.source_id == "etenders_csv"
    assert src.live is True


def test_etenders_csv_parse_mock_html():
    from tender_getter.sources.research_extra.etenders_csv import EtendersCsvSource, MOCK_HTML
    src = EtendersCsvSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_etenders_csv_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.etenders_csv import EtendersCsvSource
    src = EtendersCsvSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
