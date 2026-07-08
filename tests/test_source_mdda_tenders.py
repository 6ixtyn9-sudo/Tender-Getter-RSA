"""Tests for the Media Development and Diversity Agency (MDDA) tender source plug-in."""
import pytest


def test_mdda_tenders_source_initialization():
    from tender_getter.sources.schedule3a.mdda_tenders import MddaSource
    src = MddaSource()
    assert src.source_id == "mdda_tenders"
    assert src.live is True


def test_mdda_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.mdda_tenders import MddaSource, MOCK_HTML
    src = MddaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mdda_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.mdda_tenders import MddaSource
    src = MddaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
