"""Tests for the South African Agency for Science and Technology Advancement (SAASTA) tender source plug-in."""
import pytest


def test_saasta_source_initialization():
    from tender_getter.sources.research.saasta import SaastaSource
    src = SaastaSource()
    assert src.source_id == "saasta"
    assert src.live is True


def test_saasta_parse_mock_html():
    from tender_getter.sources.research.saasta import SaastaSource, MOCK_HTML
    src = SaastaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_saasta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.saasta import SaastaSource
    src = SaastaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
