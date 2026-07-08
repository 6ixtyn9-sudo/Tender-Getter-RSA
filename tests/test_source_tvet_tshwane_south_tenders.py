"""Tests for the Tshwane South TVET College tender source plug-in."""
import pytest


def test_tvet_tshwane_south_tenders_source_initialization():
    from tender_getter.sources.tvet.tvet_tshwane_south_tenders import TvetTshwaneSouthSource
    src = TvetTshwaneSouthSource()
    assert src.source_id == "tvet_tshwane_south_tenders"
    assert src.live is True


def test_tvet_tshwane_south_tenders_parse_mock_html():
    from tender_getter.sources.tvet.tvet_tshwane_south_tenders import TvetTshwaneSouthSource, MOCK_HTML
    src = TvetTshwaneSouthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tvet_tshwane_south_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.tvet_tshwane_south_tenders import TvetTshwaneSouthSource
    src = TvetTshwaneSouthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
