"""Tests for the Govan Mbeki Local Municipality tender source plug-in."""
import pytest


def test_govan_mbeki_lm_source_initialization():
    from tender_getter.sources.local_municipalities.govan_mbeki_lm import GovanMbekiLmSource
    src = GovanMbekiLmSource()
    assert src.source_id == "govan_mbeki_lm"
    assert isinstance(src.live, bool)


def test_govan_mbeki_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.govan_mbeki_lm import GovanMbekiLmSource, MOCK_HTML
    src = GovanMbekiLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_govan_mbeki_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.govan_mbeki_lm import GovanMbekiLmSource
    src = GovanMbekiLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
