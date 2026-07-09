"""Tests for the South African Medical Research Council (SAMRC) tender source plug-in."""
import pytest


def test_samrc_source_initialization():
    from tender_getter.sources.schedule3a.samrc import SamrcSource
    src = SamrcSource()
    assert src.source_id == "samrc"
    assert isinstance(src.live, bool)


def test_samrc_parse_mock_html():
    from tender_getter.sources.schedule3a.samrc import SamrcSource, MOCK_HTML
    src = SamrcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_samrc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.samrc import SamrcSource
    src = SamrcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
