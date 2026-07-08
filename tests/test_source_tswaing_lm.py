"""Tests for the Tswaing Local Municipality tender source plug-in."""
import pytest


def test_tswaing_lm_source_initialization():
    from tender_getter.sources.local_municipalities.tswaing_lm import TswaingLmSource
    src = TswaingLmSource()
    assert src.source_id == "tswaing_lm"
    assert src.live is True


def test_tswaing_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.tswaing_lm import TswaingLmSource, MOCK_HTML
    src = TswaingLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tswaing_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.tswaing_lm import TswaingLmSource
    src = TswaingLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
