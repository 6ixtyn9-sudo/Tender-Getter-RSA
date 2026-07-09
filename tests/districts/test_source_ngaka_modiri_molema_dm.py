"""Tests for the Ngaka Modiri Molema District Municipality tender source plug-in."""
import pytest


def test_ngaka_modiri_molema_dm_source_initialization():
    from tender_getter.sources.districts.ngaka_modiri_molema_dm import NgakaModiriMolemaDmSource
    src = NgakaModiriMolemaDmSource()
    assert src.source_id == "ngaka_modiri_molema_dm"
    assert src.live is True


def test_ngaka_modiri_molema_dm_parse_mock_html():
    from tender_getter.sources.districts.ngaka_modiri_molema_dm import NgakaModiriMolemaDmSource, MOCK_HTML
    src = NgakaModiriMolemaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ngaka_modiri_molema_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.ngaka_modiri_molema_dm import NgakaModiriMolemaDmSource
    src = NgakaModiriMolemaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
