"""Tests for the Ntabankulu (alt) tender source plug-in."""
import pytest


def test_ntabankulu_lm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ntabankulu_lm_alt_tenders import NtabankuluLmAltSource
    src = NtabankuluLmAltSource()
    assert src.source_id == "ntabankulu_lm_alt_tenders"
    assert src.live is False


def test_ntabankulu_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ntabankulu_lm_alt_tenders import NtabankuluLmAltSource, MOCK_HTML
    src = NtabankuluLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ntabankulu_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ntabankulu_lm_alt_tenders import NtabankuluLmAltSource
    src = NtabankuluLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
