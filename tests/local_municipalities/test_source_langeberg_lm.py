"""Tests for the Langeberg LM tender source plug-in."""
import pytest


def test_langeberg_lm_source_initialization():
    from tender_getter.sources.local_municipalities.langeberg_lm import LangebergLmSource
    src = LangebergLmSource()
    assert src.source_id == "langeberg_lm"
    assert isinstance(src.live, bool)


def test_langeberg_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.langeberg_lm import LangebergLmSource, MOCK_HTML
    src = LangebergLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_langeberg_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.langeberg_lm import LangebergLmSource
    src = LangebergLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
