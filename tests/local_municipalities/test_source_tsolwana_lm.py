"""Tests for the Tsolwana LM tender source plug-in."""
import pytest


def test_tsolwana_lm_source_initialization():
    from tender_getter.sources.local_municipalities.tsolwana_lm import TsolwanaLmSource
    src = TsolwanaLmSource()
    assert src.source_id == "tsolwana_lm"
    assert isinstance(src.live, bool)


def test_tsolwana_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.tsolwana_lm import TsolwanaLmSource, MOCK_HTML
    src = TsolwanaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tsolwana_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.tsolwana_lm import TsolwanaLmSource
    src = TsolwanaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
