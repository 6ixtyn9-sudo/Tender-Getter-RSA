"""Tests for the Limpopo Tourism Authority tender source plug-in."""
import pytest


def test_lp_tourism_tenders_source_initialization():
    from tender_getter.sources.research_extra.lp_tourism_tenders import LpTourismSource
    src = LpTourismSource()
    assert src.source_id == "lp_tourism_tenders"
    assert src.live is False


def test_lp_tourism_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.lp_tourism_tenders import LpTourismSource, MOCK_HTML
    src = LpTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_tourism_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.lp_tourism_tenders import LpTourismSource
    src = LpTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
