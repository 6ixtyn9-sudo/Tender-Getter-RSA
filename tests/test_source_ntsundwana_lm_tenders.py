"""Tests for the Ntsundwana LM tender source plug-in."""
import pytest


def test_ntsundwana_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ntsundwana_lm_tenders import NtsundwanaLmSource
    src = NtsundwanaLmSource()
    assert src.source_id == "ntsundwana_lm_tenders"
    assert src.live is False


def test_ntsundwana_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ntsundwana_lm_tenders import NtsundwanaLmSource, MOCK_HTML
    src = NtsundwanaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ntsundwana_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ntsundwana_lm_tenders import NtsundwanaLmSource
    src = NtsundwanaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
