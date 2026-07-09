"""Tests for the Community Schemes Ombud Service (CSOS) tender source plug-in."""
import pytest


def test_csos_source_initialization():
    from tender_getter.sources.schedule3a.csos import CsosSource
    src = CsosSource()
    assert src.source_id == "csos"
    assert isinstance(src.live, bool)


def test_csos_parse_mock_html():
    from tender_getter.sources.schedule3a.csos import CsosSource, MOCK_HTML
    src = CsosSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_csos_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.csos import CsosSource
    src = CsosSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
