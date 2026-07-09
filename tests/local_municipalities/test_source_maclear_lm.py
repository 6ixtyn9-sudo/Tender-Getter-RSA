"""Tests for the Maclear LM tender source plug-in."""
import pytest


def test_maclear_lm_source_initialization():
    from tender_getter.sources.local_municipalities.maclear_lm import MaclearLmSource
    src = MaclearLmSource()
    assert src.source_id == "maclear_lm"
    assert isinstance(src.live, bool)


def test_maclear_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.maclear_lm import MaclearLmSource, MOCK_HTML
    src = MaclearLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_maclear_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.maclear_lm import MaclearLmSource
    src = MaclearLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
