"""Tests for the Airports Company South Africa tender source plug-in."""
import pytest


def test_acsa_tenders_source_initialization():
    from tender_getter.sources.research_extra.acsa_tenders import AcsaSource
    src = AcsaSource()
    assert src.source_id == "acsa_tenders"
    assert src.live is True


def test_acsa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.acsa_tenders import AcsaSource, MOCK_HTML
    src = AcsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_acsa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.acsa_tenders import AcsaSource
    src = AcsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
