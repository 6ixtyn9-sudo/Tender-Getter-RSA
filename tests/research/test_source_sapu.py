"""Tests for the SAPU tender source plug-in."""
import pytest


def test_sapu_source_initialization():
    from tender_getter.sources.research.sapu import SapuSource
    src = SapuSource()
    assert src.source_id == "sapu"
    assert isinstance(src.live, bool)


def test_sapu_parse_mock_html():
    from tender_getter.sources.research.sapu import SapuSource, MOCK_HTML
    src = SapuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sapu_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sapu import SapuSource
    src = SapuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
