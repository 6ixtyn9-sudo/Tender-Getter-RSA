"""Tests for the Ditsobotla LM tender source plug-in."""
import pytest


def test_ditsobotla_lm_source_initialization():
    from tender_getter.sources.local_municipalities.ditsobotla_lm import DitsobotlaLmSource
    src = DitsobotlaLmSource()
    assert src.source_id == "ditsobotla_lm"
    assert isinstance(src.live, bool)


def test_ditsobotla_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.ditsobotla_lm import DitsobotlaLmSource, MOCK_HTML
    src = DitsobotlaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ditsobotla_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ditsobotla_lm import DitsobotlaLmSource
    src = DitsobotlaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
