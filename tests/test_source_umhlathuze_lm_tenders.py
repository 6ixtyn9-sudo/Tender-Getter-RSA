"""Tests for the uMhlathuze Local Municipality tender source plug-in."""
import pytest


def test_umhlathuze_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.umhlathuze_lm_tenders import UmhlathuzeLmSource
    src = UmhlathuzeLmSource()
    assert src.source_id == "umhlathuze_lm_tenders"
    assert src.live is True


def test_umhlathuze_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.umhlathuze_lm_tenders import UmhlathuzeLmSource, MOCK_HTML
    src = UmhlathuzeLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umhlathuze_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umhlathuze_lm_tenders import UmhlathuzeLmSource
    src = UmhlathuzeLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
