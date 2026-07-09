"""Tests for the Ombudsman for Short-Term Insurance tender source plug-in."""
import pytest


def test_insurance_ombud_source_initialization():
    from tender_getter.sources.regulators.insurance_ombud import InsuranceOmbudSource
    src = InsuranceOmbudSource()
    assert src.source_id == "insurance_ombud"
    assert src.live is True


def test_insurance_ombud_parse_mock_html():
    from tender_getter.sources.regulators.insurance_ombud import InsuranceOmbudSource, MOCK_HTML
    src = InsuranceOmbudSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_insurance_ombud_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.insurance_ombud import InsuranceOmbudSource
    src = InsuranceOmbudSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
