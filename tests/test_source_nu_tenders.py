"""Tests for the National Union tender source plug-in."""
import pytest


def test_nu_tenders_source_initialization():
    from tender_getter.sources.research_extra.nu_tenders import NuSource
    src = NuSource()
    assert src.source_id == "nu_tenders"
    assert src.live is False


def test_nu_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nu_tenders import NuSource, MOCK_HTML
    src = NuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nu_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nu_tenders import NuSource
    src = NuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
