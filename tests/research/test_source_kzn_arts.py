"""Tests for the KZN Arts and Culture Council tender source plug-in."""
import pytest


def test_kzn_arts_source_initialization():
    from tender_getter.sources.research.kzn_arts import KznArtsSource
    src = KznArtsSource()
    assert src.source_id == "kzn_arts"
    assert isinstance(src.live, bool)


def test_kzn_arts_parse_mock_html():
    from tender_getter.sources.research.kzn_arts import KznArtsSource, MOCK_HTML
    src = KznArtsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_arts_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.kzn_arts import KznArtsSource
    src = KznArtsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
