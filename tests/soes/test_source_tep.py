"""Tests for the Transnet Engineering (TEP) tender source plug-in."""
import pytest


def test_tep_source_initialization():
    from tender_getter.sources.soes.tep import TepSource
    src = TepSource()
    assert src.source_id == "tep"
    assert src.live is True


def test_tep_parse_mock_html():
    from tender_getter.sources.soes.tep import TepSource, MOCK_HTML
    src = TepSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tep_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.tep import TepSource
    src = TepSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
