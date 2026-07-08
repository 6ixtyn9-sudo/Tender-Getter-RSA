"""Tests for the Richards Bay (alt) tender source plug-in."""
import pytest


def test_richards_bay_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.richards_bay_lm_tenders import RichardsBayLmSource
    src = RichardsBayLmSource()
    assert src.source_id == "richards_bay_lm_tenders"
    assert src.live is False


def test_richards_bay_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.richards_bay_lm_tenders import RichardsBayLmSource, MOCK_HTML
    src = RichardsBayLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_richards_bay_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.richards_bay_lm_tenders import RichardsBayLmSource
    src = RichardsBayLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
