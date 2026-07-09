"""Tests for the Times Media tender source plug-in."""
import pytest


def test_times_media_source_initialization():
    from tender_getter.sources.research.times_media import TimesMediaSource
    src = TimesMediaSource()
    assert src.source_id == "times_media"
    assert isinstance(src.live, bool)


def test_times_media_parse_mock_html():
    from tender_getter.sources.research.times_media import TimesMediaSource, MOCK_HTML
    src = TimesMediaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_times_media_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.times_media import TimesMediaSource
    src = TimesMediaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
