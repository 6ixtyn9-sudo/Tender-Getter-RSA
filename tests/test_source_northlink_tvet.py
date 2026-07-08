"""Tests for the Northlink TVET College tender source plug-in."""
import pytest


def test_northlink_tvet_source_initialization():
    from tender_getter.sources.tvet.northlink_tvet import NorthlinkTvetSource
    src = NorthlinkTvetSource()
    assert src.source_id == "northlink_tvet"
    assert src.live is True


def test_northlink_tvet_parse_mock_html():
    from tender_getter.sources.tvet.northlink_tvet import NorthlinkTvetSource, MOCK_HTML
    src = NorthlinkTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_northlink_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.northlink_tvet import NorthlinkTvetSource
    src = NorthlinkTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
