"""Tests for the Artscape (alt URL) tender source plug-in."""
import pytest


def test_artscape_alt_tenders_source_initialization():
    from tender_getter.sources.research_extra.artscape_alt_tenders import ArtscapeAltSource
    src = ArtscapeAltSource()
    assert src.source_id == "artscape_alt_tenders"
    assert src.live is True


def test_artscape_alt_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.artscape_alt_tenders import ArtscapeAltSource, MOCK_HTML
    src = ArtscapeAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_artscape_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.artscape_alt_tenders import ArtscapeAltSource
    src = ArtscapeAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
