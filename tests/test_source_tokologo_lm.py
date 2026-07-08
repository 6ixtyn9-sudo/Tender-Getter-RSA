"""Tests for the Tokologo Local Municipality tender source plug-in."""
import pytest


def test_tokologo_lm_source_initialization():
    from tender_getter.sources.local_municipalities.tokologo_lm import TokologoLmSource
    src = TokologoLmSource()
    assert src.source_id == "tokologo_lm"
    assert src.live is True


def test_tokologo_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.tokologo_lm import TokologoLmSource, MOCK_HTML
    src = TokologoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tokologo_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.tokologo_lm import TokologoLmSource
    src = TokologoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
