"""Tests for the Fidelity ADT (public procurement) tender source plug-in."""
import pytest


def test_fidelity_tenders_source_initialization():
    from tender_getter.sources.research_extra.fidelity_tenders import FidelitySource
    src = FidelitySource()
    assert src.source_id == "fidelity_tenders"
    assert src.live is False


def test_fidelity_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.fidelity_tenders import FidelitySource, MOCK_HTML
    src = FidelitySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fidelity_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.fidelity_tenders import FidelitySource
    src = FidelitySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
