"""Tests for the Msukaligwa LM tender source plug-in."""
import pytest


def test_msukaligwa_lm_source_initialization():
    from tender_getter.sources.local_municipalities.msukaligwa_lm import MsukaligwaLmSource
    src = MsukaligwaLmSource()
    assert src.source_id == "msukaligwa_lm"
    assert isinstance(src.live, bool)


def test_msukaligwa_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.msukaligwa_lm import MsukaligwaLmSource, MOCK_HTML
    src = MsukaligwaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_msukaligwa_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.msukaligwa_lm import MsukaligwaLmSource
    src = MsukaligwaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
