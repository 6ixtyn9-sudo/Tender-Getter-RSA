"""Tests for the Artscape tender source plug-in."""
import pytest


def test_artscape_source_initialization():
    from tender_getter.sources.research.artscape import ArtscapeSource
    src = ArtscapeSource()
    assert src.source_id == "artscape"
    assert src.live is True


def test_artscape_parse_mock_html():
    from tender_getter.sources.research.artscape import ArtscapeSource, MOCK_HTML
    src = ArtscapeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_artscape_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.artscape import ArtscapeSource
    src = ArtscapeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
