"""Tests for the Makhado (alt) tender source plug-in."""
import pytest


def test_makhado_alt_2_lm_source_initialization():
    from tender_getter.sources.local_municipalities.makhado_alt_2_lm import MakhadoAlt2LmSource
    src = MakhadoAlt2LmSource()
    assert src.source_id == "makhado_alt_2_lm"
    assert isinstance(src.live, bool)


def test_makhado_alt_2_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.makhado_alt_2_lm import MakhadoAlt2LmSource, MOCK_HTML
    src = MakhadoAlt2LmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_makhado_alt_2_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.makhado_alt_2_lm import MakhadoAlt2LmSource
    src = MakhadoAlt2LmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
