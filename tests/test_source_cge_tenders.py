"""Tests for the Commission for Gender Equality (CGE) tender source plug-in."""
import pytest


def test_cge_tenders_source_initialization():
    from tender_getter.sources.chapter9.cge_tenders import CgeSource
    src = CgeSource()
    assert src.source_id == "cge_tenders"
    assert src.live is True


def test_cge_tenders_parse_mock_html():
    from tender_getter.sources.chapter9.cge_tenders import CgeSource, MOCK_HTML
    src = CgeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cge_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.cge_tenders import CgeSource
    src = CgeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
