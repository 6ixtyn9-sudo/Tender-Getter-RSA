"""Tests for the Sefako Makgatho Health Sciences University tender source plug-in."""
import pytest


def test_smu_source_initialization():
    from tender_getter.sources.universities.smu import SmuSource
    src = SmuSource()
    assert src.source_id == "smu"
    assert src.live is True


def test_smu_parse_mock_html():
    from tender_getter.sources.universities.smu import SmuSource, MOCK_HTML
    src = SmuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_smu_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.smu import SmuSource
    src = SmuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
