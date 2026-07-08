"""Tests for the Times Media tender source plug-in."""
import pytest


def test_times_media_tenders_source_initialization():
    from tender_getter.sources.research_extra.times_media_tenders import TimesMediaSource
    src = TimesMediaSource()
    assert src.source_id == "times_media_tenders"
    assert src.live is False


def test_times_media_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.times_media_tenders import TimesMediaSource, MOCK_HTML
    src = TimesMediaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_times_media_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.times_media_tenders import TimesMediaSource
    src = TimesMediaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
