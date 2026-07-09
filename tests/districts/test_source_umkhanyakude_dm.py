"""Tests for the uMkhanyakude District Municipality tender source plug-in."""
import pytest


def test_umkhanyakude_dm_source_initialization():
    from tender_getter.sources.districts.umkhanyakude_dm import UmkhanyakudeDmSource
    src = UmkhanyakudeDmSource()
    assert src.source_id == "umkhanyakude_dm"
    assert src.live is True


def test_umkhanyakude_dm_parse_mock_html():
    from tender_getter.sources.districts.umkhanyakude_dm import UmkhanyakudeDmSource, MOCK_HTML
    src = UmkhanyakudeDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umkhanyakude_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.umkhanyakude_dm import UmkhanyakudeDmSource
    src = UmkhanyakudeDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
