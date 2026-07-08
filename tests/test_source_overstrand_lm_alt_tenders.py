"""Tests for the Overstrand (alt) tender source plug-in."""
import pytest


def test_overstrand_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.overstrand_lm_alt_tenders import OverstrandLmAltSource
    src = OverstrandLmAltSource()
    assert src.source_id == "overstrand_lm_alt_tenders"
    assert src.live is True


def test_overstrand_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.overstrand_lm_alt_tenders import OverstrandLmAltSource, MOCK_HTML
    src = OverstrandLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_overstrand_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.overstrand_lm_alt_tenders import OverstrandLmAltSource
    src = OverstrandLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
