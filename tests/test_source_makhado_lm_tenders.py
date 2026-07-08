"""Tests for the Makhado Local Municipality tender source plug-in."""
import pytest


def test_makhado_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.makhado_lm_tenders import MakhadoLmSource
    src = MakhadoLmSource()
    assert src.source_id == "makhado_lm_tenders"
    assert src.live is True


def test_makhado_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.makhado_lm_tenders import MakhadoLmSource, MOCK_HTML
    src = MakhadoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_makhado_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.makhado_lm_tenders import MakhadoLmSource
    src = MakhadoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
