"""Tests for the Ditsobotla LM tender source plug-in."""
import pytest


def test_ditsobotla_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ditsobotla_lm_tenders import DitsobotlaLmSource
    src = DitsobotlaLmSource()
    assert src.source_id == "ditsobotla_lm_tenders"
    assert src.live is False


def test_ditsobotla_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ditsobotla_lm_tenders import DitsobotlaLmSource, MOCK_HTML
    src = DitsobotlaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ditsobotla_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ditsobotla_lm_tenders import DitsobotlaLmSource
    src = DitsobotlaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
