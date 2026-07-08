"""Tests for the City of Tshwane tender source plug-in."""
import pytest


def test_tshwane_tenders_source_initialization():
    from tender_getter.sources.research_extra.tshwane_tenders import TshwaneSource
    src = TshwaneSource()
    assert src.source_id == "tshwane_tenders"
    assert src.live is True


def test_tshwane_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.tshwane_tenders import TshwaneSource, MOCK_HTML
    src = TshwaneSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tshwane_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.tshwane_tenders import TshwaneSource
    src = TshwaneSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
