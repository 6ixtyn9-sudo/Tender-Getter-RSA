"""Tests for the Sekhukhune District Municipality tender source plug-in."""
import pytest


def test_sekhukhune_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.sekhukhune_dm_tenders import SekhukhuneDmSource
    src = SekhukhuneDmSource()
    assert src.source_id == "sekhukhune_dm_tenders"
    assert src.live is True


def test_sekhukhune_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.sekhukhune_dm_tenders import SekhukhuneDmSource, MOCK_HTML
    src = SekhukhuneDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sekhukhune_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.sekhukhune_dm_tenders import SekhukhuneDmSource
    src = SekhukhuneDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
