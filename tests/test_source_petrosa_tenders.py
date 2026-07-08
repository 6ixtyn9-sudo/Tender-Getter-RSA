"""Tests for the PetroSA tender source plug-in."""
import pytest


def test_petrosa_tenders_source_initialization():
    from tender_getter.sources.research_extra.petrosa_tenders import PetrosaSource
    src = PetrosaSource()
    assert src.source_id == "petrosa_tenders"
    assert src.live is True


def test_petrosa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.petrosa_tenders import PetrosaSource, MOCK_HTML
    src = PetrosaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_petrosa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.petrosa_tenders import PetrosaSource
    src = PetrosaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
