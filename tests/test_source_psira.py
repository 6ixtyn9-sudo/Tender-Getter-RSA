"""Tests for the Private Security Industry Regulatory Authority (PSIRA) tender source plug-in."""
import pytest


def test_psira_source_initialization():
    from tender_getter.sources.schedule3a.psira import PsiraSource
    src = PsiraSource()
    assert src.source_id == "psira"
    assert src.live is True


def test_psira_parse_mock_html():
    from tender_getter.sources.schedule3a.psira import PsiraSource, MOCK_HTML
    src = PsiraSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_psira_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.psira import PsiraSource
    src = PsiraSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
