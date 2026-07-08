"""Tests for the Gert Sibande District Municipality tender source plug-in."""
import pytest


def test_gert_sibande_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.gert_sibande_dm_tenders import GertSibandeDmSource
    src = GertSibandeDmSource()
    assert src.source_id == "gert_sibande_dm_tenders"
    assert src.live is True


def test_gert_sibande_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.gert_sibande_dm_tenders import GertSibandeDmSource, MOCK_HTML
    src = GertSibandeDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gert_sibande_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.gert_sibande_dm_tenders import GertSibandeDmSource
    src = GertSibandeDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
