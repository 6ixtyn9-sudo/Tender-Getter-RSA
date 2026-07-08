"""Tests for the Blue Gum LM tender source plug-in."""
import pytest


def test_blue_gum_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.blue_gum_lm_tenders import BlueGumLmSource
    src = BlueGumLmSource()
    assert src.source_id == "blue_gum_lm_tenders"
    assert src.live is False


def test_blue_gum_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.blue_gum_lm_tenders import BlueGumLmSource, MOCK_HTML
    src = BlueGumLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_blue_gum_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.blue_gum_lm_tenders import BlueGumLmSource
    src = BlueGumLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
