"""Tests for the Siyancuma LM tender source plug-in."""
import pytest


def test_siyancuma_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.siyancuma_lm_tenders import SiyancumaLmSource
    src = SiyancumaLmSource()
    assert src.source_id == "siyancuma_lm_tenders"
    assert src.live is False


def test_siyancuma_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.siyancuma_lm_tenders import SiyancumaLmSource, MOCK_HTML
    src = SiyancumaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_siyancuma_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.siyancuma_lm_tenders import SiyancumaLmSource
    src = SiyancumaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
