"""Tests for the uMuziwabantu LM tender source plug-in."""
import pytest


def test_umuziwabantu_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.umuziwabantu_lm_tenders import UmuziwabantuLmSource
    src = UmuziwabantuLmSource()
    assert src.source_id == "umuziwabantu_lm_tenders"
    assert src.live is False


def test_umuziwabantu_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.umuziwabantu_lm_tenders import UmuziwabantuLmSource, MOCK_HTML
    src = UmuziwabantuLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umuziwabantu_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umuziwabantu_lm_tenders import UmuziwabantuLmSource
    src = UmuziwabantuLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
