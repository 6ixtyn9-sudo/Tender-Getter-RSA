"""Tests for the Emfuleni Local Municipality tender source plug-in."""
import pytest


def test_emfuleni_lm_source_initialization():
    from tender_getter.sources.local_municipalities.emfuleni_lm import EmfuleniLmSource
    src = EmfuleniLmSource()
    assert src.source_id == "emfuleni_lm"
    assert src.live is True


def test_emfuleni_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.emfuleni_lm import EmfuleniLmSource, MOCK_HTML
    src = EmfuleniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_emfuleni_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.emfuleni_lm import EmfuleniLmSource
    src = EmfuleniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
