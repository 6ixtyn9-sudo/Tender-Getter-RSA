"""Tests for the Insurance Institute tender source plug-in."""
import pytest


def test_insurance_institute_source_initialization():
    from tender_getter.sources.research.insurance_institute import InsuranceInstituteSource
    src = InsuranceInstituteSource()
    assert src.source_id == "insurance_institute"
    assert isinstance(src.live, bool)


def test_insurance_institute_parse_mock_html():
    from tender_getter.sources.research.insurance_institute import InsuranceInstituteSource, MOCK_HTML
    src = InsuranceInstituteSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_insurance_institute_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.insurance_institute import InsuranceInstituteSource
    src = InsuranceInstituteSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
