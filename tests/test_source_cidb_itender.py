"""Tests for the CIDB i-Tender tender source plug-in."""
import pytest


def test_cidb_itender_source_initialization():
    from tender_getter.sources.research_extra.cidb_itender import CidbItenderSource
    src = CidbItenderSource()
    assert src.source_id == "cidb_itender"
    assert src.live is True


def test_cidb_itender_parse_mock_html():
    from tender_getter.sources.research_extra.cidb_itender import CidbItenderSource, MOCK_HTML
    src = CidbItenderSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cidb_itender_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.cidb_itender import CidbItenderSource
    src = CidbItenderSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
