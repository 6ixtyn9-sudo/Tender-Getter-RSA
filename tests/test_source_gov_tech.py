"""Tests for the GovTech SA tender source plug-in."""
import pytest


def test_gov_tech_source_initialization():
    from tender_getter.sources.local_municipalities.gov_tech import GovTechSource
    src = GovTechSource()
    assert src.source_id == "gov_tech"
    assert src.live is False


def test_gov_tech_parse_mock_html():
    from tender_getter.sources.local_municipalities.gov_tech import GovTechSource, MOCK_HTML
    src = GovTechSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gov_tech_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.gov_tech import GovTechSource
    src = GovTechSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
