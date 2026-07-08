"""Tests for the National Energy Regulator of South Africa (NERSA) tender source plug-in."""
import pytest


def test_nersa_tenders_source_initialization():
    from tender_getter.sources.schedule3a.nersa_tenders import NersaSource
    src = NersaSource()
    assert src.source_id == "nersa_tenders"
    assert src.live is True


def test_nersa_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.nersa_tenders import NersaSource, MOCK_HTML
    src = NersaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nersa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nersa_tenders import NersaSource
    src = NersaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
