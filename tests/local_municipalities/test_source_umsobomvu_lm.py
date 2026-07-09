"""Tests for the Umsobomvu LM tender source plug-in."""
import pytest


def test_umsobomvu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.umsobomvu_lm import UmsobomvuLmSource
    src = UmsobomvuLmSource()
    assert src.source_id == "umsobomvu_lm"
    assert isinstance(src.live, bool)


def test_umsobomvu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.umsobomvu_lm import UmsobomvuLmSource, MOCK_HTML
    src = UmsobomvuLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umsobomvu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umsobomvu_lm import UmsobomvuLmSource
    src = UmsobomvuLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
