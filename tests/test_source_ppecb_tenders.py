"""Tests for the Perishable Products Export Control Board (PPECB) tender source plug-in."""
import pytest


def test_ppecb_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ppecb_tenders import PpecbSource
    src = PpecbSource()
    assert src.source_id == "ppecb_tenders"
    assert src.live is True


def test_ppecb_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ppecb_tenders import PpecbSource, MOCK_HTML
    src = PpecbSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ppecb_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ppecb_tenders import PpecbSource
    src = PpecbSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
