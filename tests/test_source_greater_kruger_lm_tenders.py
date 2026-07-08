"""Tests for the Greater Kruger LM tender source plug-in."""
import pytest


def test_greater_kruger_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.greater_kruger_lm_tenders import GreaterKrugerLmSource
    src = GreaterKrugerLmSource()
    assert src.source_id == "greater_kruger_lm_tenders"
    assert src.live is False


def test_greater_kruger_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.greater_kruger_lm_tenders import GreaterKrugerLmSource, MOCK_HTML
    src = GreaterKrugerLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_greater_kruger_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.greater_kruger_lm_tenders import GreaterKrugerLmSource
    src = GreaterKrugerLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
