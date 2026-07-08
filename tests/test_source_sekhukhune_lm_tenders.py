"""Tests for the Sekhukhune LM tender source plug-in."""
import pytest


def test_sekhukhune_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.sekhukhune_lm_tenders import SekhukhuneLmSource
    src = SekhukhuneLmSource()
    assert src.source_id == "sekhukhune_lm_tenders"
    assert src.live is False


def test_sekhukhune_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.sekhukhune_lm_tenders import SekhukhuneLmSource, MOCK_HTML
    src = SekhukhuneLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sekhukhune_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.sekhukhune_lm_tenders import SekhukhuneLmSource
    src = SekhukhuneLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
