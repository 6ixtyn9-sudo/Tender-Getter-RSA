"""Tests for the National Student Financial Aid Scheme (NSFAS) tender source plug-in."""
import pytest


def test_nsfas_source_initialization():
    from tender_getter.sources.schedule3a.nsfas import NsfasSource
    src = NsfasSource()
    assert src.source_id == "nsfas"
    assert isinstance(src.live, bool)


def test_nsfas_parse_mock_html():
    from tender_getter.sources.schedule3a.nsfas import NsfasSource, MOCK_HTML
    src = NsfasSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nsfas_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nsfas import NsfasSource
    src = NsfasSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
