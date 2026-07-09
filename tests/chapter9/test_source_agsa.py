"""Tests for the Auditor-General South Africa (AGSA) tender source plug-in."""
import pytest


def test_agsa_source_initialization():
    from tender_getter.sources.chapter9.agsa import AgsaSource
    src = AgsaSource()
    assert src.source_id == "agsa"
    assert isinstance(src.live, bool)


def test_agsa_parse_mock_html():
    from tender_getter.sources.chapter9.agsa import AgsaSource, MOCK_HTML
    src = AgsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_agsa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.agsa import AgsaSource
    src = AgsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
