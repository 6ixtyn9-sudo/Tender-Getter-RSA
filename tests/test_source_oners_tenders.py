"""Tests for the Office of the Registrar of Agricultural Inputs tender source plug-in."""
import pytest


def test_oners_tenders_source_initialization():
    from tender_getter.sources.research_extra.oners_tenders import OnersSource
    src = OnersSource()
    assert src.source_id == "oners_tenders"
    assert src.live is False


def test_oners_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.oners_tenders import OnersSource, MOCK_HTML
    src = OnersSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_oners_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.oners_tenders import OnersSource
    src = OnersSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
