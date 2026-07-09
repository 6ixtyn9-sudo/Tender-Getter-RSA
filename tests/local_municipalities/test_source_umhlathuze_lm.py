"""Tests for the uMhlathuze Local Municipality tender source plug-in."""
import pytest


def test_umhlathuze_lm_source_initialization():
    from tender_getter.sources.local_municipalities.umhlathuze_lm import UmhlathuzeLmSource
    src = UmhlathuzeLmSource()
    assert src.source_id == "umhlathuze_lm"
    assert isinstance(src.live, bool)


def test_umhlathuze_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.umhlathuze_lm import UmhlathuzeLmSource, MOCK_HTML
    src = UmhlathuzeLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umhlathuze_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umhlathuze_lm import UmhlathuzeLmSource
    src = UmhlathuzeLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
