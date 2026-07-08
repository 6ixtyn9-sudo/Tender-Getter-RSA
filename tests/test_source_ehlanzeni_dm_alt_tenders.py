"""Tests for the Ehlanzeni (DM alt URL) tender source plug-in."""
import pytest


def test_ehlanzeni_dm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ehlanzeni_dm_alt_tenders import EhlanzeniDmAltSource
    src = EhlanzeniDmAltSource()
    assert src.source_id == "ehlanzeni_dm_alt_tenders"
    assert src.live is False


def test_ehlanzeni_dm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ehlanzeni_dm_alt_tenders import EhlanzeniDmAltSource, MOCK_HTML
    src = EhlanzeniDmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ehlanzeni_dm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ehlanzeni_dm_alt_tenders import EhlanzeniDmAltSource
    src = EhlanzeniDmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
