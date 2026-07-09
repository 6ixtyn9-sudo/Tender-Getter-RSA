"""Tests for the City of Joburg Property Company (JPC) SOC tender source plug-in."""
import pytest


def test_coj_property_company_source_initialization():
    from tender_getter.sources.local_municipalities.coj_property_company import CojPropertyCompanySource
    src = CojPropertyCompanySource()
    assert src.source_id == "coj_property_company"
    assert isinstance(src.live, bool)


def test_coj_property_company_parse_mock_html():
    from tender_getter.sources.local_municipalities.coj_property_company import CojPropertyCompanySource, MOCK_HTML
    src = CojPropertyCompanySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_coj_property_company_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.coj_property_company import CojPropertyCompanySource
    src = CojPropertyCompanySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
