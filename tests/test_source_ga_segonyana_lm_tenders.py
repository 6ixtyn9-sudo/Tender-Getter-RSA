"""Tests for the Ga-Segonyana Local Municipality tender source plug-in."""
import pytest


def test_ga_segonyana_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ga_segonyana_lm_tenders import GaSegonyanaLmSource
    src = GaSegonyanaLmSource()
    assert src.source_id == "ga_segonyana_lm_tenders"
    assert src.live is True


def test_ga_segonyana_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ga_segonyana_lm_tenders import GaSegonyanaLmSource, MOCK_HTML
    src = GaSegonyanaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ga_segonyana_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ga_segonyana_lm_tenders import GaSegonyanaLmSource
    src = GaSegonyanaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
