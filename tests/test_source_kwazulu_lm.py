"""Tests for the Kwazulu LM tender source plug-in."""
import pytest


def test_kwazulu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.kwazulu_lm import KwazuluLmSource
    src = KwazuluLmSource()
    assert src.source_id == "kwazulu_lm"
    assert src.live is False


def test_kwazulu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.kwazulu_lm import KwazuluLmSource, MOCK_HTML
    src = KwazuluLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kwazulu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.kwazulu_lm import KwazuluLmSource
    src = KwazuluLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
