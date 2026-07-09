"""Tests for the South African Heritage Resources Agency (SAHRA) tender source plug-in."""
import pytest


def test_sahra_source_initialization():
    from tender_getter.sources.research.sahra import SahraSource
    src = SahraSource()
    assert src.source_id == "sahra"
    assert isinstance(src.live, bool)


def test_sahra_parse_mock_html():
    from tender_getter.sources.research.sahra import SahraSource, MOCK_HTML
    src = SahraSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sahra_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sahra import SahraSource
    src = SahraSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
