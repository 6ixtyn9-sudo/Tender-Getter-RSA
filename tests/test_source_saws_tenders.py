"""Tests for the South African Weather Service (SAWS) tender source plug-in."""
import pytest


def test_saws_tenders_source_initialization():
    from tender_getter.sources.research_extra.saws_tenders import SawsSource
    src = SawsSource()
    assert src.source_id == "saws_tenders"
    assert src.live is True


def test_saws_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.saws_tenders import SawsSource, MOCK_HTML
    src = SawsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_saws_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.saws_tenders import SawsSource
    src = SawsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
