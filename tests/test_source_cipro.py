"""Tests for the CIPRO (legacy CIPC) tender source plug-in."""
import pytest


def test_cipro_source_initialization():
    from tender_getter.sources.research.cipro import CiproSource
    src = CiproSource()
    assert src.source_id == "cipro"
    assert src.live is False


def test_cipro_parse_mock_html():
    from tender_getter.sources.research.cipro import CiproSource, MOCK_HTML
    src = CiproSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cipro_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.cipro import CiproSource
    src = CiproSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
