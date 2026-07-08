"""Tests for the Ehlanzeni District Municipality tender source plug-in."""
import pytest


def test_ehlanzeni_tenders_source_initialization():
    from tender_getter.sources.research_extra.ehlanzeni_tenders import EhlanzeniSource
    src = EhlanzeniSource()
    assert src.source_id == "ehlanzeni_tenders"
    assert src.live is True


def test_ehlanzeni_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ehlanzeni_tenders import EhlanzeniSource, MOCK_HTML
    src = EhlanzeniSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ehlanzeni_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ehlanzeni_tenders import EhlanzeniSource
    src = EhlanzeniSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
