"""Tests for the Legal Aid SA (alt URL) tender source plug-in."""
import pytest


def test_legal_aid_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.legal_aid_alt_tenders import LegalAidAltSource
    src = LegalAidAltSource()
    assert src.source_id == "legal_aid_alt_tenders"
    assert src.live is True


def test_legal_aid_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.legal_aid_alt_tenders import LegalAidAltSource, MOCK_HTML
    src = LegalAidAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_legal_aid_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.legal_aid_alt_tenders import LegalAidAltSource
    src = LegalAidAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
