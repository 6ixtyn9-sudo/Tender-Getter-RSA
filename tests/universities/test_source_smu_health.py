"""Tests for the Sefako Makgatho Health Sciences University (alternate) tender source plug-in."""
import pytest


def test_smu_health_source_initialization():
    from tender_getter.sources.universities.smu_health import SmuHealthSource
    src = SmuHealthSource()
    assert src.source_id == "smu_health"
    assert isinstance(src.live, bool)


def test_smu_health_parse_mock_html():
    from tender_getter.sources.universities.smu_health import SmuHealthSource, MOCK_HTML
    src = SmuHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_smu_health_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.smu_health import SmuHealthSource
    src = SmuHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
