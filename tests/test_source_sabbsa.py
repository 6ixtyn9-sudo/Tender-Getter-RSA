"""Tests for the SABBSA tender source plug-in."""
import pytest


def test_sabbsa_source_initialization():
    from tender_getter.sources.research.sabbsa import SabbsaSource
    src = SabbsaSource()
    assert src.source_id == "sabbsa"
    assert src.live is False


def test_sabbsa_parse_mock_html():
    from tender_getter.sources.research.sabbsa import SabbsaSource, MOCK_HTML
    src = SabbsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sabbsa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sabbsa import SabbsaSource
    src = SabbsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
