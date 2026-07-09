"""Tests for the Richards Bay (alt) tender source plug-in."""
import pytest


def test_richards_bay_lm_source_initialization():
    from tender_getter.sources.local_municipalities.richards_bay_lm import RichardsBayLmSource
    src = RichardsBayLmSource()
    assert src.source_id == "richards_bay_lm"
    assert isinstance(src.live, bool)


def test_richards_bay_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.richards_bay_lm import RichardsBayLmSource, MOCK_HTML
    src = RichardsBayLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_richards_bay_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.richards_bay_lm import RichardsBayLmSource
    src = RichardsBayLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
