"""Tests for the Denel Land Systems tender source plug-in."""
import pytest


def test_denel_land_systems_source_initialization():
    from tender_getter.sources.soes.denel_land_systems import DenelLandSystemsSource
    src = DenelLandSystemsSource()
    assert src.source_id == "denel_land_systems"
    assert isinstance(src.live, bool)


def test_denel_land_systems_parse_mock_html():
    from tender_getter.sources.soes.denel_land_systems import DenelLandSystemsSource, MOCK_HTML
    src = DenelLandSystemsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_denel_land_systems_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.denel_land_systems import DenelLandSystemsSource
    src = DenelLandSystemsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
