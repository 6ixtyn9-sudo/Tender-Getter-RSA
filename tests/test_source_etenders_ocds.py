"""Tests for the National Treasury eTenders OCDS API tender source plug-in."""
import pytest


def test_etenders_ocds_source_initialization():
    from tender_getter.sources.research_extra.etenders_ocds import EtendersOcdsSource
    src = EtendersOcdsSource()
    assert src.source_id == "etenders_ocds"
    assert src.live is True


def test_etenders_ocds_parse_mock_html():
    from tender_getter.sources.research_extra.etenders_ocds import EtendersOcdsSource, MOCK_HTML
    src = EtendersOcdsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_etenders_ocds_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.etenders_ocds import EtendersOcdsSource
    src = EtendersOcdsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
