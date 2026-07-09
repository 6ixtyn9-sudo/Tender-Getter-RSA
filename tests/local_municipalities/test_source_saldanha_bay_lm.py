"""Tests for the Saldanha Bay Municipality tender source plug-in."""
import pytest


def test_saldanha_bay_lm_source_initialization():
    from tender_getter.sources.local_municipalities.saldanha_bay_lm import SaldanhaBayLmSource
    src = SaldanhaBayLmSource()
    assert src.source_id == "saldanha_bay_lm"
    assert src.live is True


def test_saldanha_bay_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.saldanha_bay_lm import SaldanhaBayLmSource, MOCK_HTML
    src = SaldanhaBayLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_saldanha_bay_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.saldanha_bay_lm import SaldanhaBayLmSource
    src = SaldanhaBayLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
