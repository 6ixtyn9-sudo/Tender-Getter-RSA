"""Tests for the Centre for Public Service Innovation (CPSI) tender source plug-in."""
import pytest


def test_cpsi_source_initialization():
    from tender_getter.sources.schedule3a.cpsi import CpsiSource
    src = CpsiSource()
    assert src.source_id == "cpsi"
    assert src.live is True


def test_cpsi_parse_mock_html():
    from tender_getter.sources.schedule3a.cpsi import CpsiSource, MOCK_HTML
    src = CpsiSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cpsi_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.cpsi import CpsiSource
    src = CpsiSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
