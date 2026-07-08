"""Tests for the PRASA Intersite Asset Management tender source plug-in."""
import pytest


def test_intersite_tenders_source_initialization():
    from tender_getter.sources.soes_extra.intersite_tenders import IntersiteSource
    src = IntersiteSource()
    assert src.source_id == "intersite_tenders"
    assert src.live is True


def test_intersite_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.intersite_tenders import IntersiteSource, MOCK_HTML
    src = IntersiteSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_intersite_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.intersite_tenders import IntersiteSource
    src = IntersiteSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
