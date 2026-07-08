"""Tests for the Mpumalanga Investment tender source plug-in."""
import pytest


def test_mp_invest_source_initialization():
    from tender_getter.sources.research.mp_invest import MpInvestSource
    src = MpInvestSource()
    assert src.source_id == "mp_invest"
    assert src.live is False


def test_mp_invest_parse_mock_html():
    from tender_getter.sources.research.mp_invest import MpInvestSource, MOCK_HTML
    src = MpInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_invest_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.mp_invest import MpInvestSource
    src = MpInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
