"""Tests for the Tshwane North TVET College tender source plug-in."""
import pytest


def test_tvet_tshwane_north_tenders_source_initialization():
    from tender_getter.sources.tvet.tvet_tshwane_north_tenders import TvetTshwaneNorthSource
    src = TvetTshwaneNorthSource()
    assert src.source_id == "tvet_tshwane_north_tenders"
    assert src.live is True


def test_tvet_tshwane_north_tenders_parse_mock_html():
    from tender_getter.sources.tvet.tvet_tshwane_north_tenders import TvetTshwaneNorthSource, MOCK_HTML
    src = TvetTshwaneNorthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tvet_tshwane_north_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.tvet_tshwane_north_tenders import TvetTshwaneNorthSource
    src = TvetTshwaneNorthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
