"""Tests for the Ezemvelo KZN Wildlife tender source plug-in."""
import pytest


def test_kzn_wildlife_source_initialization():
    from tender_getter.sources.research.kzn_wildlife import KznWildlifeSource
    src = KznWildlifeSource()
    assert src.source_id == "kzn_wildlife"
    assert isinstance(src.live, bool)


def test_kzn_wildlife_parse_mock_html():
    from tender_getter.sources.research.kzn_wildlife import KznWildlifeSource, MOCK_HTML
    src = KznWildlifeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_wildlife_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.kzn_wildlife import KznWildlifeSource
    src = KznWildlifeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
