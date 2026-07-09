"""Tests for the Mantsopa Local Municipality tender source plug-in."""
import pytest


def test_manuawe_lm_source_initialization():
    from tender_getter.sources.local_municipalities.manuawe_lm import ManuaweLmSource
    src = ManuaweLmSource()
    assert src.source_id == "manuawe_lm"
    assert isinstance(src.live, bool)


def test_manuawe_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.manuawe_lm import ManuaweLmSource, MOCK_HTML
    src = ManuaweLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_manuawe_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.manuawe_lm import ManuaweLmSource
    src = ManuaweLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
