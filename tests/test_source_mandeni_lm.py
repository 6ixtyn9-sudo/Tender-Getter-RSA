"""Tests for the Mandeni LM tender source plug-in."""
import pytest


def test_mandeni_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mandeni_lm import MandeniLmSource
    src = MandeniLmSource()
    assert src.source_id == "mandeni_lm"
    assert src.live is False


def test_mandeni_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mandeni_lm import MandeniLmSource, MOCK_HTML
    src = MandeniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mandeni_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mandeni_lm import MandeniLmSource
    src = MandeniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
