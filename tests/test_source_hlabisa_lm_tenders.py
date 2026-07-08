"""Tests for the Hlabisa LM tender source plug-in."""
import pytest


def test_hlabisa_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.hlabisa_lm_tenders import HlabisaLmSource
    src = HlabisaLmSource()
    assert src.source_id == "hlabisa_lm_tenders"
    assert src.live is False


def test_hlabisa_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.hlabisa_lm_tenders import HlabisaLmSource, MOCK_HTML
    src = HlabisaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_hlabisa_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.hlabisa_lm_tenders import HlabisaLmSource
    src = HlabisaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
