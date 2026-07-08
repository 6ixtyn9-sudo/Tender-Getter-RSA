"""Tests for the Lejweleputswa District Municipality tender source plug-in."""
import pytest


def test_lejweleputswa_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.lejweleputswa_dm_tenders import LejweleputswaDmSource
    src = LejweleputswaDmSource()
    assert src.source_id == "lejweleputswa_dm_tenders"
    assert src.live is True


def test_lejweleputswa_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.lejweleputswa_dm_tenders import LejweleputswaDmSource, MOCK_HTML
    src = LejweleputswaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lejweleputswa_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.lejweleputswa_dm_tenders import LejweleputswaDmSource
    src = LejweleputswaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
