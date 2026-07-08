"""Tests for the Ugu District Municipality tender source plug-in."""
import pytest


def test_ugu_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.ugu_dm_tenders import UguDmSource
    src = UguDmSource()
    assert src.source_id == "ugu_dm_tenders"
    assert src.live is True


def test_ugu_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.ugu_dm_tenders import UguDmSource, MOCK_HTML
    src = UguDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ugu_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.ugu_dm_tenders import UguDmSource
    src = UguDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
