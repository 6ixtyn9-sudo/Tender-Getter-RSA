"""Tests for the Fidelity ADT (public procurement) tender source plug-in."""
import pytest


def test_fidelity_source_initialization():
    from tender_getter.sources.research.fidelity import FidelitySource
    src = FidelitySource()
    assert src.source_id == "fidelity"
    assert isinstance(src.live, bool)


def test_fidelity_parse_mock_html():
    from tender_getter.sources.research.fidelity import FidelitySource, MOCK_HTML
    src = FidelitySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fidelity_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fidelity import FidelitySource
    src = FidelitySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
