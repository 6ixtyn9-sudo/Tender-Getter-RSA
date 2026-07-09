"""Tests for the Drakenstein Municipality tender source plug-in."""
import pytest


def test_drakenstein_lm_source_initialization():
    from tender_getter.sources.local_municipalities.drakenstein_lm import DrakensteinLmSource
    src = DrakensteinLmSource()
    assert src.source_id == "drakenstein_lm"
    assert src.live is True


def test_drakenstein_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.drakenstein_lm import DrakensteinLmSource, MOCK_HTML
    src = DrakensteinLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_drakenstein_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.drakenstein_lm import DrakensteinLmSource
    src = DrakensteinLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
