"""Tests for the South African National Accreditation System (SANAS) tender source plug-in."""
import pytest


def test_sanas_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sanas_tenders import SanasSource
    src = SanasSource()
    assert src.source_id == "sanas_tenders"
    assert src.live is True


def test_sanas_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sanas_tenders import SanasSource, MOCK_HTML
    src = SanasSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanas_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sanas_tenders import SanasSource
    src = SanasSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
