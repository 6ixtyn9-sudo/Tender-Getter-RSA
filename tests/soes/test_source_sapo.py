"""Tests for the South African Post Office (SAPO) tender source plug-in."""
import pytest


def test_sapo_source_initialization():
    from tender_getter.sources.soes.sapo import SapoSource
    src = SapoSource()
    assert src.source_id == "sapo"
    assert isinstance(src.live, bool)


def test_sapo_parse_mock_html():
    from tender_getter.sources.soes.sapo import SapoSource, MOCK_HTML
    src = SapoSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sapo_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.sapo import SapoSource
    src = SapoSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
