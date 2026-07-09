"""Tests for the Aberdeen Plain LM tender source plug-in."""
import pytest


def test_aberdeen_plain_lm_source_initialization():
    from tender_getter.sources.local_municipalities.aberdeen_plain_lm import AberdeenPlainLmSource
    src = AberdeenPlainLmSource()
    assert src.source_id == "aberdeen_plain_lm"
    assert isinstance(src.live, bool)


def test_aberdeen_plain_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.aberdeen_plain_lm import AberdeenPlainLmSource, MOCK_HTML
    src = AberdeenPlainLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_aberdeen_plain_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.aberdeen_plain_lm import AberdeenPlainLmSource
    src = AberdeenPlainLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
