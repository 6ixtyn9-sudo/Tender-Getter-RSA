"""Tests for the Greater Lebowakgomo LM tender source plug-in."""
import pytest


def test_greater_lebowakgomo_lm_source_initialization():
    from tender_getter.sources.local_municipalities.greater_lebowakgomo_lm import GreaterLebowakgomoLmSource
    src = GreaterLebowakgomoLmSource()
    assert src.source_id == "greater_lebowakgomo_lm"
    assert isinstance(src.live, bool)


def test_greater_lebowakgomo_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.greater_lebowakgomo_lm import GreaterLebowakgomoLmSource, MOCK_HTML
    src = GreaterLebowakgomoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_greater_lebowakgomo_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.greater_lebowakgomo_lm import GreaterLebowakgomoLmSource
    src = GreaterLebowakgomoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
