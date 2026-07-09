"""Tests for the Capricorn TVET College tender source plug-in."""
import pytest


def test_capricorn_tvet_source_initialization():
    from tender_getter.sources.tvet.capricorn_tvet import CapricornTvetSource
    src = CapricornTvetSource()
    assert src.source_id == "capricorn_tvet"
    assert src.live is True


def test_capricorn_tvet_parse_mock_html():
    from tender_getter.sources.tvet.capricorn_tvet import CapricornTvetSource, MOCK_HTML
    src = CapricornTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_capricorn_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.capricorn_tvet import CapricornTvetSource
    src = CapricornTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
