"""Tests for the Mossel Bay Municipality tender source plug-in."""
import pytest


def test_mossel_bay_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mossel_bay_lm import MosselBayLmSource
    src = MosselBayLmSource()
    assert src.source_id == "mossel_bay_lm"
    assert src.live is True


def test_mossel_bay_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mossel_bay_lm import MosselBayLmSource, MOCK_HTML
    src = MosselBayLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mossel_bay_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mossel_bay_lm import MosselBayLmSource
    src = MosselBayLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
