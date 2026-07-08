"""Tests for the Limpopo Department of Public Works, Roads & Infrastructure tender source plug-in."""
import pytest


def test_limpopo_pwri_tenders_source_initialization():
    from tender_getter.sources.research_extra.limpopo_pwri_tenders import LimpopoPwriSource
    src = LimpopoPwriSource()
    assert src.source_id == "limpopo_pwri_tenders"
    assert src.live is True


def test_limpopo_pwri_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.limpopo_pwri_tenders import LimpopoPwriSource, MOCK_HTML
    src = LimpopoPwriSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_limpopo_pwri_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.limpopo_pwri_tenders import LimpopoPwriSource
    src = LimpopoPwriSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
