"""Tests for the Midvaal Local Municipality tender source plug-in."""
import pytest


def test_midvaal_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.midvaal_lm_tenders import MidvaalLmSource
    src = MidvaalLmSource()
    assert src.source_id == "midvaal_lm_tenders"
    assert src.live is True


def test_midvaal_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.midvaal_lm_tenders import MidvaalLmSource, MOCK_HTML
    src = MidvaalLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_midvaal_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.midvaal_lm_tenders import MidvaalLmSource
    src = MidvaalLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
