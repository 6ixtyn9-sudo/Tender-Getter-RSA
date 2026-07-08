"""Tests for the Legal Aid SA tender source plug-in."""
import pytest


def test_legal_aid_sa_tenders_source_initialization():
    from tender_getter.sources.research_extra.legal_aid_sa_tenders import LegalAidSaSource
    src = LegalAidSaSource()
    assert src.source_id == "legal_aid_sa_tenders"
    assert src.live is True


def test_legal_aid_sa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.legal_aid_sa_tenders import LegalAidSaSource, MOCK_HTML
    src = LegalAidSaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_legal_aid_sa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.legal_aid_sa_tenders import LegalAidSaSource
    src = LegalAidSaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
