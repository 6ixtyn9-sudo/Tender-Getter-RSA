"""Tests for the Masilonyana Local Municipality tender source plug-in."""
import pytest


def test_masilonyana_lm_source_initialization():
    from tender_getter.sources.local_municipalities.masilonyana_lm import MasilonyanaLmSource
    src = MasilonyanaLmSource()
    assert src.source_id == "masilonyana_lm"
    assert src.live is True


def test_masilonyana_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.masilonyana_lm import MasilonyanaLmSource, MOCK_HTML
    src = MasilonyanaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_masilonyana_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.masilonyana_lm import MasilonyanaLmSource
    src = MasilonyanaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
