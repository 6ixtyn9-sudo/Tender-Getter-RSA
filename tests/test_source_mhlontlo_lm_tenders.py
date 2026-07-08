"""Tests for the Mhlontlo LM tender source plug-in."""
import pytest


def test_mhlontlo_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.mhlontlo_lm_tenders import MhlontloLmSource
    src = MhlontloLmSource()
    assert src.source_id == "mhlontlo_lm_tenders"
    assert src.live is False


def test_mhlontlo_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.mhlontlo_lm_tenders import MhlontloLmSource, MOCK_HTML
    src = MhlontloLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mhlontlo_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mhlontlo_lm_tenders import MhlontloLmSource
    src = MhlontloLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
