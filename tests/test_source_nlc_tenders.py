"""Tests for the National Lotteries Commission (NLC) tender source plug-in."""
import pytest


def test_nlc_tenders_source_initialization():
    from tender_getter.sources.research_extra.nlc_tenders import NlcSource
    src = NlcSource()
    assert src.source_id == "nlc_tenders"
    assert src.live is True


def test_nlc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nlc_tenders import NlcSource, MOCK_HTML
    src = NlcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nlc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nlc_tenders import NlcSource
    src = NlcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
