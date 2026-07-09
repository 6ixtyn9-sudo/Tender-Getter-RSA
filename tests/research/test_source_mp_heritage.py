"""Tests for the Mpumalanga Heritage tender source plug-in."""
import pytest


def test_mp_heritage_source_initialization():
    from tender_getter.sources.research.mp_heritage import MpHeritageSource
    src = MpHeritageSource()
    assert src.source_id == "mp_heritage"
    assert src.live is False


def test_mp_heritage_parse_mock_html():
    from tender_getter.sources.research.mp_heritage import MpHeritageSource, MOCK_HTML
    src = MpHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_heritage_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.mp_heritage import MpHeritageSource
    src = MpHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
