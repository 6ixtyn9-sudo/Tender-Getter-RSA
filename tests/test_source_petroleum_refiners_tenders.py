"""Tests for the National Petroleum Refiners (Natref) tender source plug-in."""
import pytest


def test_petroleum_refiners_tenders_source_initialization():
    from tender_getter.sources.research_extra.petroleum_refiners_tenders import PetroleumRefinersSource
    src = PetroleumRefinersSource()
    assert src.source_id == "petroleum_refiners_tenders"
    assert src.live is False


def test_petroleum_refiners_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.petroleum_refiners_tenders import PetroleumRefinersSource, MOCK_HTML
    src = PetroleumRefinersSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_petroleum_refiners_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.petroleum_refiners_tenders import PetroleumRefinersSource
    src = PetroleumRefinersSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
