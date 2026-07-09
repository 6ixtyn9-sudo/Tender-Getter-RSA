"""Tests for the NG (alt) tender source plug-in."""
import pytest


def test_national_gambling_source_initialization():
    from tender_getter.sources.research.national_gambling import NationalGamblingSource
    src = NationalGamblingSource()
    assert src.source_id == "national_gambling"
    assert isinstance(src.live, bool)


def test_national_gambling_parse_mock_html():
    from tender_getter.sources.research.national_gambling import NationalGamblingSource, MOCK_HTML
    src = NationalGamblingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_national_gambling_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.national_gambling import NationalGamblingSource
    src = NationalGamblingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
