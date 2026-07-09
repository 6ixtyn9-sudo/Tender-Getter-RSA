"""Tests for the Greater Letaba LM tender source plug-in."""
import pytest


def test_greater_letaba_lm_source_initialization():
    from tender_getter.sources.local_municipalities.greater_letaba_lm import GreaterLetabaLmSource
    src = GreaterLetabaLmSource()
    assert src.source_id == "greater_letaba_lm"
    assert isinstance(src.live, bool)


def test_greater_letaba_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.greater_letaba_lm import GreaterLetabaLmSource, MOCK_HTML
    src = GreaterLetabaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_greater_letaba_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.greater_letaba_lm import GreaterLetabaLmSource
    src = GreaterLetabaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
