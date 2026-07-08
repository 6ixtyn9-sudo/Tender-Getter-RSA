"""Tests for the Karoo Hoogland LM tender source plug-in."""
import pytest


def test_karoo_hoogland_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.karoo_hoogland_lm_tenders import KarooHooglandLmSource
    src = KarooHooglandLmSource()
    assert src.source_id == "karoo_hoogland_lm_tenders"
    assert src.live is False


def test_karoo_hoogland_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.karoo_hoogland_lm_tenders import KarooHooglandLmSource, MOCK_HTML
    src = KarooHooglandLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_karoo_hoogland_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.karoo_hoogland_lm_tenders import KarooHooglandLmSource
    src = KarooHooglandLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
