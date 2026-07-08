"""Tests for the City of Johannesburg tender source plug-in."""
import pytest


def test_johannesburg_tenders_source_initialization():
    from tender_getter.sources.research_extra.johannesburg_tenders import JohannesburgSource
    src = JohannesburgSource()
    assert src.source_id == "johannesburg_tenders"
    assert src.live is True


def test_johannesburg_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.johannesburg_tenders import JohannesburgSource, MOCK_HTML
    src = JohannesburgSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_johannesburg_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.johannesburg_tenders import JohannesburgSource
    src = JohannesburgSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
