"""Tests for the uMvoti LM tender source plug-in."""
import pytest


def test_umvoti_lm_source_initialization():
    from tender_getter.sources.local_municipalities.umvoti_lm import UmvotiLmSource
    src = UmvotiLmSource()
    assert src.source_id == "umvoti_lm"
    assert src.live is False


def test_umvoti_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.umvoti_lm import UmvotiLmSource, MOCK_HTML
    src = UmvotiLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umvoti_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umvoti_lm import UmvotiLmSource
    src = UmvotiLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
