"""Tests for the SABBSA tender source plug-in."""
import pytest


def test_sabbsa_tenders_source_initialization():
    from tender_getter.sources.research_extra.sabbsa_tenders import SabbsaSource
    src = SabbsaSource()
    assert src.source_id == "sabbsa_tenders"
    assert src.live is False


def test_sabbsa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sabbsa_tenders import SabbsaSource, MOCK_HTML
    src = SabbsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sabbsa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sabbsa_tenders import SabbsaSource
    src = SabbsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
