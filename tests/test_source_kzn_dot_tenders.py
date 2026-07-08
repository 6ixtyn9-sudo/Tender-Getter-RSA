"""Tests for the KwaZulu-Natal Department of Transport tender source plug-in."""
import pytest


def test_kzn_dot_tenders_source_initialization():
    from tender_getter.sources.research_extra.kzn_dot_tenders import KznDotSource
    src = KznDotSource()
    assert src.source_id == "kzn_dot_tenders"
    assert src.live is True


def test_kzn_dot_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.kzn_dot_tenders import KznDotSource, MOCK_HTML
    src = KznDotSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_dot_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.kzn_dot_tenders import KznDotSource
    src = KznDotSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
