"""Tests for the Health Professions Council of South Africa (HPCSA) tender source plug-in."""
import pytest


def test_hcps_source_initialization():
    from tender_getter.sources.research.hcps import HcpsSource
    src = HcpsSource()
    assert src.source_id == "hcps"
    assert src.live is True


def test_hcps_parse_mock_html():
    from tender_getter.sources.research.hcps import HcpsSource, MOCK_HTML
    src = HcpsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_hcps_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.hcps import HcpsSource
    src = HcpsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
