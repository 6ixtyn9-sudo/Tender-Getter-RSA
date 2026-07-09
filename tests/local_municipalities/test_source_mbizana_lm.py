"""Tests for the Mbizana LM tender source plug-in."""
import pytest


def test_mbizana_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mbizana_lm import MbizanaLmSource
    src = MbizanaLmSource()
    assert src.source_id == "mbizana_lm"
    assert src.live is False


def test_mbizana_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mbizana_lm import MbizanaLmSource, MOCK_HTML
    src = MbizanaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mbizana_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mbizana_lm import MbizanaLmSource
    src = MbizanaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
