"""Tests for the Armscor (Armaments Corporation of SA) tender source plug-in."""
import pytest


def test_armscor_source_initialization():
    from tender_getter.sources.soes.armscor import ArmscorSource
    src = ArmscorSource()
    assert src.source_id == "armscor"
    assert isinstance(src.live, bool)


def test_armscor_parse_mock_html():
    from tender_getter.sources.soes.armscor import ArmscorSource, MOCK_HTML
    src = ArmscorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_armscor_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.armscor import ArmscorSource
    src = ArmscorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
