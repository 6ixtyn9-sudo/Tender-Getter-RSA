"""Tests for the Makhado (alt 2) tender source plug-in."""
import pytest


def test_makhado_lm_alt_2_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.makhado_lm_alt_2_tenders import MakhadoLmAlt2Source
    src = MakhadoLmAlt2Source()
    assert src.source_id == "makhado_lm_alt_2_tenders"
    assert src.live is False


def test_makhado_lm_alt_2_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.makhado_lm_alt_2_tenders import MakhadoLmAlt2Source, MOCK_HTML
    src = MakhadoLmAlt2Source()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_makhado_lm_alt_2_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.makhado_lm_alt_2_tenders import MakhadoLmAlt2Source
    src = MakhadoLmAlt2Source()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
