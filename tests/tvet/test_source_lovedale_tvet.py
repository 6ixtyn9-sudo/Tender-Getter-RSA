"""Tests for the Lovedale TVET College tender source plug-in."""
import pytest


def test_lovedale_tvet_source_initialization():
    from tender_getter.sources.tvet.lovedale_tvet import LovedaleTvetSource
    src = LovedaleTvetSource()
    assert src.source_id == "lovedale_tvet"
    assert isinstance(src.live, bool)


def test_lovedale_tvet_parse_mock_html():
    from tender_getter.sources.tvet.lovedale_tvet import LovedaleTvetSource, MOCK_HTML
    src = LovedaleTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lovedale_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.lovedale_tvet import LovedaleTvetSource
    src = LovedaleTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
