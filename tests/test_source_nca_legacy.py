"""Tests for the National Consumer Agency (legacy) tender source plug-in."""
import pytest


def test_nca_legacy_source_initialization():
    from tender_getter.sources.schedule3a.nca_legacy import NcaLegacySource
    src = NcaLegacySource()
    assert src.source_id == "nca_legacy"
    assert src.live is False


def test_nca_legacy_parse_mock_html():
    from tender_getter.sources.schedule3a.nca_legacy import NcaLegacySource, MOCK_HTML
    src = NcaLegacySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nca_legacy_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nca_legacy import NcaLegacySource
    src = NcaLegacySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
