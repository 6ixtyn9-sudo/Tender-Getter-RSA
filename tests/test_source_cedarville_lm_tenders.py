"""Tests for the Cedarville LM tender source plug-in."""
import pytest


def test_cedarville_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.cedarville_lm_tenders import CedarvilleLmSource
    src = CedarvilleLmSource()
    assert src.source_id == "cedarville_lm_tenders"
    assert src.live is False


def test_cedarville_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.cedarville_lm_tenders import CedarvilleLmSource, MOCK_HTML
    src = CedarvilleLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cedarville_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.cedarville_lm_tenders import CedarvilleLmSource
    src = CedarvilleLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
