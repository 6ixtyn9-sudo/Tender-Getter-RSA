"""Tests for the Greater Tubatse LM tender source plug-in."""
import pytest


def test_greater_tubatse_lm_source_initialization():
    from tender_getter.sources.local_municipalities.greater_tubatse_lm import GreaterTubatseLmSource
    src = GreaterTubatseLmSource()
    assert src.source_id == "greater_tubatse_lm"
    assert isinstance(src.live, bool)


def test_greater_tubatse_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.greater_tubatse_lm import GreaterTubatseLmSource, MOCK_HTML
    src = GreaterTubatseLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_greater_tubatse_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.greater_tubatse_lm import GreaterTubatseLmSource
    src = GreaterTubatseLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
