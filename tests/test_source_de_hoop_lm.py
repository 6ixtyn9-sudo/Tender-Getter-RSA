"""Tests for the De Hoop LM tender source plug-in."""
import pytest


def test_de_hoop_lm_source_initialization():
    from tender_getter.sources.local_municipalities.de_hoop_lm import DeHoopLmSource
    src = DeHoopLmSource()
    assert src.source_id == "de_hoop_lm"
    assert src.live is False


def test_de_hoop_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.de_hoop_lm import DeHoopLmSource, MOCK_HTML
    src = DeHoopLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_de_hoop_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.de_hoop_lm import DeHoopLmSource
    src = DeHoopLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
