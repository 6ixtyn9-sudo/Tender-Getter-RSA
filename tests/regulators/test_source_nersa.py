"""Tests for the National Energy Regulator of South Africa (NERSA) tender source plug-in."""
import pytest


def test_nersa_source_initialization():
    from tender_getter.sources.regulators.nersa import NersaSource
    src = NersaSource()
    assert src.source_id == "nersa"
    assert src.live is True


def test_nersa_parse_mock_html():
    from tender_getter.sources.regulators.nersa import NersaSource, MOCK_HTML
    src = NersaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nersa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.nersa import NersaSource
    src = NersaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
