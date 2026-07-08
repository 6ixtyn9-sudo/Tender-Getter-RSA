"""Tests for the Limpopo Heritage Foundation tender source plug-in."""
import pytest


def test_lp_heritage_tenders_source_initialization():
    from tender_getter.sources.research_extra.lp_heritage_tenders import LpHeritageSource
    src = LpHeritageSource()
    assert src.source_id == "lp_heritage_tenders"
    assert src.live is False


def test_lp_heritage_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.lp_heritage_tenders import LpHeritageSource, MOCK_HTML
    src = LpHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_heritage_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.lp_heritage_tenders import LpHeritageSource
    src = LpHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
