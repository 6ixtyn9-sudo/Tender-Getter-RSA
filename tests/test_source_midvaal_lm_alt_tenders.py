"""Tests for the Midvaal (alt) tender source plug-in."""
import pytest


def test_midvaal_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.midvaal_lm_alt_tenders import MidvaalLmAltSource
    src = MidvaalLmAltSource()
    assert src.source_id == "midvaal_lm_alt_tenders"
    assert src.live is True


def test_midvaal_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.midvaal_lm_alt_tenders import MidvaalLmAltSource, MOCK_HTML
    src = MidvaalLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_midvaal_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.midvaal_lm_alt_tenders import MidvaalLmAltSource
    src = MidvaalLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
