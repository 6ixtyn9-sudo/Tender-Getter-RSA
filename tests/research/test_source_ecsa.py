"""Tests for the ECSA tender source plug-in."""
import pytest


def test_ecsa_source_initialization():
    from tender_getter.sources.research.ecsa import EcsaSource
    src = EcsaSource()
    assert src.source_id == "ecsa"
    assert isinstance(src.live, bool)


def test_ecsa_parse_mock_html():
    from tender_getter.sources.research.ecsa import EcsaSource, MOCK_HTML
    src = EcsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ecsa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ecsa import EcsaSource
    src = EcsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
