"""Tests for the Strategic Fuel Fund (SFF) tender source plug-in."""
import pytest


def test_sff_source_initialization():
    from tender_getter.sources.soes.sff import SffSource
    src = SffSource()
    assert src.source_id == "sff"
    assert src.live is True


def test_sff_parse_mock_html():
    from tender_getter.sources.soes.sff import SffSource, MOCK_HTML
    src = SffSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sff_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.sff import SffSource
    src = SffSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
