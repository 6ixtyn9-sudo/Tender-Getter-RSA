"""Tests for the Diamond LM tender source plug-in."""
import pytest


def test_diamond_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.diamond_lm_tenders import DiamondLmSource
    src = DiamondLmSource()
    assert src.source_id == "diamond_lm_tenders"
    assert src.live is False


def test_diamond_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.diamond_lm_tenders import DiamondLmSource, MOCK_HTML
    src = DiamondLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_diamond_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.diamond_lm_tenders import DiamondLmSource
    src = DiamondLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
