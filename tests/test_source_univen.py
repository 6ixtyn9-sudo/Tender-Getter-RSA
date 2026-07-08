"""Tests for the University of Venda tender source plug-in."""
import pytest


def test_univen_source_initialization():
    from tender_getter.sources.universities.univen import UnivenSource
    src = UnivenSource()
    assert src.source_id == "univen"
    assert src.live is True


def test_univen_parse_mock_html():
    from tender_getter.sources.universities.univen import UnivenSource, MOCK_HTML
    src = UnivenSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_univen_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.univen import UnivenSource
    src = UnivenSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
