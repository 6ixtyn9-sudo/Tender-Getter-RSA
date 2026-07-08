"""Tests for the Maletswai LM tender source plug-in."""
import pytest


def test_maletswai_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.maletswai_lm_tenders import MaletswaiLmSource
    src = MaletswaiLmSource()
    assert src.source_id == "maletswai_lm_tenders"
    assert src.live is False


def test_maletswai_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.maletswai_lm_tenders import MaletswaiLmSource, MOCK_HTML
    src = MaletswaiLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_maletswai_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.maletswai_lm_tenders import MaletswaiLmSource
    src = MaletswaiLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
