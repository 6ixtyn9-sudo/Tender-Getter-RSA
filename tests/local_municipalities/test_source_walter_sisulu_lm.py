"""Tests for the Walter Sisulu LM tender source plug-in."""
import pytest


def test_walter_sisulu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.walter_sisulu_lm import WalterSisuluLmSource
    src = WalterSisuluLmSource()
    assert src.source_id == "walter_sisulu_lm"
    assert isinstance(src.live, bool)


def test_walter_sisulu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.walter_sisulu_lm import WalterSisuluLmSource, MOCK_HTML
    src = WalterSisuluLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_walter_sisulu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.walter_sisulu_lm import WalterSisuluLmSource
    src = WalterSisuluLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
