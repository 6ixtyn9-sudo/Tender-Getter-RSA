"""Tests for the Moqhaka LM tender source plug-in."""
import pytest


def test_moqhaka_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.moqhaka_lm_tenders import MoqhakaLmSource
    src = MoqhakaLmSource()
    assert src.source_id == "moqhaka_lm_tenders"
    assert src.live is False


def test_moqhaka_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.moqhaka_lm_tenders import MoqhakaLmSource, MOCK_HTML
    src = MoqhakaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_moqhaka_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.moqhaka_lm_tenders import MoqhakaLmSource
    src = MoqhakaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
