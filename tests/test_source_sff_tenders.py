"""Tests for the Strategic Fuel Fund (SFF) tender source plug-in."""
import pytest


def test_sff_tenders_source_initialization():
    from tender_getter.sources.soes_extra.sff_tenders import SffSource
    src = SffSource()
    assert src.source_id == "sff_tenders"
    assert src.live is True


def test_sff_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.sff_tenders import SffSource, MOCK_HTML
    src = SffSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sff_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.sff_tenders import SffSource
    src = SffSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
