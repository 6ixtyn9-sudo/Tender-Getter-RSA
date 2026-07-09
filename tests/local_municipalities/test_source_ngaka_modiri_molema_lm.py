"""Tests for the Ngaka Modiri Molema DM tender source plug-in."""
import pytest


def test_ngaka_modiri_molema_lm_source_initialization():
    from tender_getter.sources.local_municipalities.ngaka_modiri_molema_lm import NgakaModiriMolemaLmSource
    src = NgakaModiriMolemaLmSource()
    assert src.source_id == "ngaka_modiri_molema_lm"
    assert src.live is True


def test_ngaka_modiri_molema_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.ngaka_modiri_molema_lm import NgakaModiriMolemaLmSource, MOCK_HTML
    src = NgakaModiriMolemaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ngaka_modiri_molema_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ngaka_modiri_molema_lm import NgakaModiriMolemaLmSource
    src = NgakaModiriMolemaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
