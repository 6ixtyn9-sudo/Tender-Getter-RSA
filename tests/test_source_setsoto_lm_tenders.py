"""Tests for the Setsoto LM tender source plug-in."""
import pytest


def test_setsoto_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.setsoto_lm_tenders import SetsotoLmSource
    src = SetsotoLmSource()
    assert src.source_id == "setsoto_lm_tenders"
    assert src.live is False


def test_setsoto_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.setsoto_lm_tenders import SetsotoLmSource, MOCK_HTML
    src = SetsotoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_setsoto_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.setsoto_lm_tenders import SetsotoLmSource
    src = SetsotoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
