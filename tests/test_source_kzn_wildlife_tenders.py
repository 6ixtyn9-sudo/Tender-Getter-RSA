"""Tests for the Ezemvelo KZN Wildlife tender source plug-in."""
import pytest


def test_kzn_wildlife_tenders_source_initialization():
    from tender_getter.sources.research_extra.kzn_wildlife_tenders import KznWildlifeSource
    src = KznWildlifeSource()
    assert src.source_id == "kzn_wildlife_tenders"
    assert src.live is True


def test_kzn_wildlife_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.kzn_wildlife_tenders import KznWildlifeSource, MOCK_HTML
    src = KznWildlifeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_wildlife_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.kzn_wildlife_tenders import KznWildlifeSource
    src = KznWildlifeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
