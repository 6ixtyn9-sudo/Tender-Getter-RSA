"""Tests for the National Lotteries Commission (NLC) tender source plug-in."""
import pytest


def test_nlc_source_initialization():
    from tender_getter.sources.research.nlc import NlcSource
    src = NlcSource()
    assert src.source_id == "nlc"
    assert isinstance(src.live, bool)


def test_nlc_parse_mock_html():
    from tender_getter.sources.research.nlc import NlcSource, MOCK_HTML
    src = NlcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nlc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nlc import NlcSource
    src = NlcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
