"""Tests for the Denel Aerostructures (SOC) Ltd tender source plug-in."""
import pytest


def test_denel_aerostructures_source_initialization():
    from tender_getter.sources.soes.denel_aerostructures import DenelAerostructuresSource
    src = DenelAerostructuresSource()
    assert src.source_id == "denel_aerostructures"
    assert isinstance(src.live, bool)


def test_denel_aerostructures_parse_mock_html():
    from tender_getter.sources.soes.denel_aerostructures import DenelAerostructuresSource, MOCK_HTML
    src = DenelAerostructuresSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_denel_aerostructures_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.denel_aerostructures import DenelAerostructuresSource
    src = DenelAerostructuresSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
