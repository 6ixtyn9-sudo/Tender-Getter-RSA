"""Tests for the Nyandeni LM tender source plug-in."""
import pytest


def test_nyandeni_lm_source_initialization():
    from tender_getter.sources.local_municipalities.nyandeni_lm import NyandeniLmSource
    src = NyandeniLmSource()
    assert src.source_id == "nyandeni_lm"
    assert src.live is False


def test_nyandeni_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.nyandeni_lm import NyandeniLmSource, MOCK_HTML
    src = NyandeniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nyandeni_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.nyandeni_lm import NyandeniLmSource
    src = NyandeniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
