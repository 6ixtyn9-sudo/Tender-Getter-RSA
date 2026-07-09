"""Tests for the Ugu District Municipality tender source plug-in."""
import pytest


def test_ugu_dm_source_initialization():
    from tender_getter.sources.districts.ugu_dm import UguDmSource
    src = UguDmSource()
    assert src.source_id == "ugu_dm"
    assert src.live is True


def test_ugu_dm_parse_mock_html():
    from tender_getter.sources.districts.ugu_dm import UguDmSource, MOCK_HTML
    src = UguDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ugu_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.ugu_dm import UguDmSource
    src = UguDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
