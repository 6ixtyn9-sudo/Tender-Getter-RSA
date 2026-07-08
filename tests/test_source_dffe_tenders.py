"""Tests for the Department of Forestry, Fisheries & the Environment tender source plug-in."""
import pytest


def test_dffe_tenders_source_initialization():
    from tender_getter.sources.research_extra.dffe_tenders import DffeSource
    src = DffeSource()
    assert src.source_id == "dffe_tenders"
    assert src.live is True


def test_dffe_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dffe_tenders import DffeSource, MOCK_HTML
    src = DffeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dffe_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dffe_tenders import DffeSource
    src = DffeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
