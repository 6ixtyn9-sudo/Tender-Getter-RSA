"""Tests for the uMzimkhulu LM tender source plug-in."""
import pytest


def test_umzimkhulu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.umzimkhulu_lm import UmzimkhuluLmSource
    src = UmzimkhuluLmSource()
    assert src.source_id == "umzimkhulu_lm"
    assert src.live is False


def test_umzimkhulu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.umzimkhulu_lm import UmzimkhuluLmSource, MOCK_HTML
    src = UmzimkhuluLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umzimkhulu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umzimkhulu_lm import UmzimkhuluLmSource
    src = UmzimkhuluLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
