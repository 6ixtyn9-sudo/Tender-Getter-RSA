"""Tests for the South African Maritime Safety Authority tender source plug-in."""
import pytest


def test_samsa_tenders_source_initialization():
    from tender_getter.sources.research_extra.samsa_tenders import SamsaSource
    src = SamsaSource()
    assert src.source_id == "samsa_tenders"
    assert src.live is True


def test_samsa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.samsa_tenders import SamsaSource, MOCK_HTML
    src = SamsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_samsa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.samsa_tenders import SamsaSource
    src = SamsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
