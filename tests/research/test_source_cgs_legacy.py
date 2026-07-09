"""Tests for the Council for Geoscience (legacy URL) tender source plug-in."""
import pytest


def test_cgs_legacy_source_initialization():
    from tender_getter.sources.research.cgs_legacy import CgsLegacySource
    src = CgsLegacySource()
    assert src.source_id == "cgs_legacy"
    assert isinstance(src.live, bool)


def test_cgs_legacy_parse_mock_html():
    from tender_getter.sources.research.cgs_legacy import CgsLegacySource, MOCK_HTML
    src = CgsLegacySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cgs_legacy_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.cgs_legacy import CgsLegacySource
    src = CgsLegacySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
