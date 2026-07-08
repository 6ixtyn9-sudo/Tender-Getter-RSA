"""Tests for the Oostenberg Municipality (legacy) tender source plug-in."""
import pytest


def test_oostenberg_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.oostenberg_lm_tenders import OostenbergLmSource
    src = OostenbergLmSource()
    assert src.source_id == "oostenberg_lm_tenders"
    assert src.live is False


def test_oostenberg_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.oostenberg_lm_tenders import OostenbergLmSource, MOCK_HTML
    src = OostenbergLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_oostenberg_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.oostenberg_lm_tenders import OostenbergLmSource
    src = OostenbergLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
