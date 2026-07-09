"""Tests for the Legal Aid SA tender source plug-in."""
import pytest


def test_legal_aid_sa_source_initialization():
    from tender_getter.sources.research.legal_aid_sa import LegalAidSaSource
    src = LegalAidSaSource()
    assert src.source_id == "legal_aid_sa"
    assert src.live is True


def test_legal_aid_sa_parse_mock_html():
    from tender_getter.sources.research.legal_aid_sa import LegalAidSaSource, MOCK_HTML
    src = LegalAidSaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_legal_aid_sa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.legal_aid_sa import LegalAidSaSource
    src = LegalAidSaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
