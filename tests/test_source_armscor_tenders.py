"""Tests for the Armscor (Armaments Corporation of SA) tender source plug-in."""
import pytest


def test_armscor_tenders_source_initialization():
    from tender_getter.sources.soes_extra.armscor_tenders import ArmscorSource
    src = ArmscorSource()
    assert src.source_id == "armscor_tenders"
    assert src.live is True


def test_armscor_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.armscor_tenders import ArmscorSource, MOCK_HTML
    src = ArmscorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_armscor_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.armscor_tenders import ArmscorSource
    src = ArmscorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
