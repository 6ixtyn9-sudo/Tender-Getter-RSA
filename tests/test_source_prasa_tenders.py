"""Tests for the Passenger Rail Agency of South Africa (PRASA) tender source plug-in."""
import pytest


def test_prasa_tenders_source_initialization():
    from tender_getter.sources.research_extra.prasa_tenders import PrasaSource
    src = PrasaSource()
    assert src.source_id == "prasa_tenders"
    assert src.live is True


def test_prasa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.prasa_tenders import PrasaSource, MOCK_HTML
    src = PrasaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_prasa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.prasa_tenders import PrasaSource
    src = PrasaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
