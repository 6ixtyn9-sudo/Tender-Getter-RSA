"""Tests for the Modimolle (alt) tender source plug-in."""
import pytest


def test_modimolle_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.modimolle_lm_alt_tenders import ModimolleLmAltSource
    src = ModimolleLmAltSource()
    assert src.source_id == "modimolle_lm_alt_tenders"
    assert src.live is False


def test_modimolle_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.modimolle_lm_alt_tenders import ModimolleLmAltSource, MOCK_HTML
    src = ModimolleLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_modimolle_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.modimolle_lm_alt_tenders import ModimolleLmAltSource
    src = ModimolleLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
