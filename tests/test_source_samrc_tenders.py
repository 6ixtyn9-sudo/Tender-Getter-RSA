"""Tests for the South African Medical Research Council (SAMRC) tender source plug-in."""
import pytest


def test_samrc_tenders_source_initialization():
    from tender_getter.sources.schedule3a.samrc_tenders import SamrcSource
    src = SamrcSource()
    assert src.source_id == "samrc_tenders"
    assert src.live is True


def test_samrc_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.samrc_tenders import SamrcSource, MOCK_HTML
    src = SamrcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_samrc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.samrc_tenders import SamrcSource
    src = SamrcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
