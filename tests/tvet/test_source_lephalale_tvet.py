"""Tests for the Lephalale TVET tender source plug-in."""
import pytest


def test_lephalale_tvet_source_initialization():
    from tender_getter.sources.tvet.lephalale_tvet import LephalaleTvetSource
    src = LephalaleTvetSource()
    assert src.source_id == "lephalale_tvet"
    assert src.live is True


def test_lephalale_tvet_parse_mock_html():
    from tender_getter.sources.tvet.lephalale_tvet import LephalaleTvetSource, MOCK_HTML
    src = LephalaleTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lephalale_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.lephalale_tvet import LephalaleTvetSource
    src = LephalaleTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
