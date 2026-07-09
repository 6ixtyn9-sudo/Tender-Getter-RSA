"""Tests for the Commission for Gender Equality (CGE) tender source plug-in."""
import pytest


def test_cge_source_initialization():
    from tender_getter.sources.chapter9.cge import CgeSource
    src = CgeSource()
    assert src.source_id == "cge"
    assert isinstance(src.live, bool)


def test_cge_parse_mock_html():
    from tender_getter.sources.chapter9.cge import CgeSource, MOCK_HTML
    src = CgeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cge_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.cge import CgeSource
    src = CgeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
