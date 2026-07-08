"""Tests for the Indaka LM tender source plug-in."""
import pytest


def test_indaka_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.indaka_lm_tenders import IndakaLmSource
    src = IndakaLmSource()
    assert src.source_id == "indaka_lm_tenders"
    assert src.live is False


def test_indaka_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.indaka_lm_tenders import IndakaLmSource, MOCK_HTML
    src = IndakaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_indaka_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.indaka_lm_tenders import IndakaLmSource
    src = IndakaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
