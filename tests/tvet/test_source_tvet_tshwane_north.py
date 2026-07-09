"""Tests for the Tshwane North TVET College tender source plug-in."""
import pytest


def test_tvet_tshwane_north_source_initialization():
    from tender_getter.sources.tvet.tvet_tshwane_north import TvetTshwaneNorthSource
    src = TvetTshwaneNorthSource()
    assert src.source_id == "tvet_tshwane_north"
    assert isinstance(src.live, bool)


def test_tvet_tshwane_north_parse_mock_html():
    from tender_getter.sources.tvet.tvet_tshwane_north import TvetTshwaneNorthSource, MOCK_HTML
    src = TvetTshwaneNorthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tvet_tshwane_north_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.tvet_tshwane_north import TvetTshwaneNorthSource
    src = TvetTshwaneNorthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
