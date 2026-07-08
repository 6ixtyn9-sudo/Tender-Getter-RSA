"""Tests for the ECSA tender source plug-in."""
import pytest


def test_ecsa_tenders_source_initialization():
    from tender_getter.sources.research_extra.ecsa_tenders import EcsaSource
    src = EcsaSource()
    assert src.source_id == "ecsa_tenders"
    assert src.live is True


def test_ecsa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ecsa_tenders import EcsaSource, MOCK_HTML
    src = EcsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ecsa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ecsa_tenders import EcsaSource
    src = EcsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
