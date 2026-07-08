"""Tests for the Ephraim Mogale (alt) tender source plug-in."""
import pytest


def test_ephraim_mogale_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ephraim_mogale_lm_alt_tenders import EphraimMogaleLmAltSource
    src = EphraimMogaleLmAltSource()
    assert src.source_id == "ephraim_mogale_lm_alt_tenders"
    assert src.live is False


def test_ephraim_mogale_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ephraim_mogale_lm_alt_tenders import EphraimMogaleLmAltSource, MOCK_HTML
    src = EphraimMogaleLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ephraim_mogale_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ephraim_mogale_lm_alt_tenders import EphraimMogaleLmAltSource
    src = EphraimMogaleLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
