"""Tests for the Bela-Bela LM tender source plug-in."""
import pytest


def test_bela_bela_lm_source_initialization():
    from tender_getter.sources.local_municipalities.bela_bela_lm import BelaBelaLmSource
    src = BelaBelaLmSource()
    assert src.source_id == "bela_bela_lm"
    assert src.live is False


def test_bela_bela_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.bela_bela_lm import BelaBelaLmSource, MOCK_HTML
    src = BelaBelaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_bela_bela_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.bela_bela_lm import BelaBelaLmSource
    src = BelaBelaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
