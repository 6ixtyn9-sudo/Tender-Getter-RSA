"""Tests for the Health Professions Council of South Africa (HPCSA) tender source plug-in."""
import pytest


def test_hcpsa_source_initialization():
    from tender_getter.sources.schedule3a.hcpsa import HcpsaSource
    src = HcpsaSource()
    assert src.source_id == "hcpsa"
    assert src.live is True


def test_hcpsa_parse_mock_html():
    from tender_getter.sources.schedule3a.hcpsa import HcpsaSource, MOCK_HTML
    src = HcpsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_hcpsa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.hcpsa import HcpsaSource
    src = HcpsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
