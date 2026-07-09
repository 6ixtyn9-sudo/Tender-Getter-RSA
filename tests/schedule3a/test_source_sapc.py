"""Tests for the South African Pharmacy Council (SAPC) tender source plug-in."""
import pytest


def test_sapc_source_initialization():
    from tender_getter.sources.schedule3a.sapc import SapcSource
    src = SapcSource()
    assert src.source_id == "sapc"
    assert src.live is True


def test_sapc_parse_mock_html():
    from tender_getter.sources.schedule3a.sapc import SapcSource, MOCK_HTML
    src = SapcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sapc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sapc import SapcSource
    src = SapcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
