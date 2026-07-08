"""Tests for the Sefako Makgatho Health Sciences University (alternate) tender source plug-in."""
import pytest


def test_smu_health_tenders_source_initialization():
    from tender_getter.sources.universities.smu_health_tenders import SmuHealthSource
    src = SmuHealthSource()
    assert src.source_id == "smu_health_tenders"
    assert src.live is True


def test_smu_health_tenders_parse_mock_html():
    from tender_getter.sources.universities.smu_health_tenders import SmuHealthSource, MOCK_HTML
    src = SmuHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_smu_health_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.smu_health_tenders import SmuHealthSource
    src = SmuHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
