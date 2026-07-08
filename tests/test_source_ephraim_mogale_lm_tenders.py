"""Tests for the Ephraim Mogale Local Municipality tender source plug-in."""
import pytest


def test_ephraim_mogale_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ephraim_mogale_lm_tenders import EphraimMogaleLmSource
    src = EphraimMogaleLmSource()
    assert src.source_id == "ephraim_mogale_lm_tenders"
    assert src.live is True


def test_ephraim_mogale_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ephraim_mogale_lm_tenders import EphraimMogaleLmSource, MOCK_HTML
    src = EphraimMogaleLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ephraim_mogale_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ephraim_mogale_lm_tenders import EphraimMogaleLmSource
    src = EphraimMogaleLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
