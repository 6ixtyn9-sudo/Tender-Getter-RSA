"""Tests for the uMzimvubu LM tender source plug-in."""
import pytest


def test_umzimvubu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.umzimvubu_lm import UmzimvubuLmSource
    src = UmzimvubuLmSource()
    assert src.source_id == "umzimvubu_lm"
    assert isinstance(src.live, bool)


def test_umzimvubu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.umzimvubu_lm import UmzimvubuLmSource, MOCK_HTML
    src = UmzimvubuLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umzimvubu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umzimvubu_lm import UmzimvubuLmSource
    src = UmzimvubuLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
