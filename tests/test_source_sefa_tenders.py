"""Tests for the Small Enterprise Finance Agency tender source plug-in."""
import pytest


def test_sefa_tenders_source_initialization():
    from tender_getter.sources.research_extra.sefa_tenders import SefaSource
    src = SefaSource()
    assert src.source_id == "sefa_tenders"
    assert src.live is True


def test_sefa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sefa_tenders import SefaSource, MOCK_HTML
    src = SefaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sefa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sefa_tenders import SefaSource
    src = SefaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
