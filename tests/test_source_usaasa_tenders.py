"""Tests for the Universal Service and Access Agency of South Africa (USAASA) tender source plug-in."""
import pytest


def test_usaasa_tenders_source_initialization():
    from tender_getter.sources.schedule3a.usaasa_tenders import UsaasaSource
    src = UsaasaSource()
    assert src.source_id == "usaasa_tenders"
    assert src.live is True


def test_usaasa_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.usaasa_tenders import UsaasaSource, MOCK_HTML
    src = UsaasaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_usaasa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.usaasa_tenders import UsaasaSource
    src = UsaasaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
