"""Tests for the University of Pretoria tender source plug-in."""
import pytest


def test_up_source_initialization():
    from tender_getter.sources.universities.up import UpSource
    src = UpSource()
    assert src.source_id == "up"
    assert src.live is True


def test_up_parse_mock_html():
    from tender_getter.sources.universities.up import UpSource, MOCK_HTML
    src = UpSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_up_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.up import UpSource
    src = UpSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
