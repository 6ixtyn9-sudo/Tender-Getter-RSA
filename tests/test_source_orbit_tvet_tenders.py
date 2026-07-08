"""Tests for the Orbit TVET College tender source plug-in."""
import pytest


def test_orbit_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.orbit_tvet_tenders import OrbitTvetSource
    src = OrbitTvetSource()
    assert src.source_id == "orbit_tvet_tenders"
    assert src.live is True


def test_orbit_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.orbit_tvet_tenders import OrbitTvetSource, MOCK_HTML
    src = OrbitTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_orbit_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.orbit_tvet_tenders import OrbitTvetSource
    src = OrbitTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
