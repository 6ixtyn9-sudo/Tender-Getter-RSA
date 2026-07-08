"""Tests for the SARS (alt URL 2) tender source plug-in."""
import pytest


def test_sars_alt_2_tenders_source_initialization():
    from tender_getter.sources.research_extra.sars_alt_2_tenders import SarsAlt2Source
    src = SarsAlt2Source()
    assert src.source_id == "sars_alt_2_tenders"
    assert src.live is True


def test_sars_alt_2_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sars_alt_2_tenders import SarsAlt2Source, MOCK_HTML
    src = SarsAlt2Source()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sars_alt_2_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sars_alt_2_tenders import SarsAlt2Source
    src = SarsAlt2Source()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
