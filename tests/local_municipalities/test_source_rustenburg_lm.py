"""Tests for the Rustenburg Local Municipality tender source plug-in."""
import pytest


def test_rustenburg_lm_source_initialization():
    from tender_getter.sources.local_municipalities.rustenburg_lm import RustenburgLmSource
    src = RustenburgLmSource()
    assert src.source_id == "rustenburg_lm"
    assert isinstance(src.live, bool)


def test_rustenburg_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.rustenburg_lm import RustenburgLmSource, MOCK_HTML
    src = RustenburgLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_rustenburg_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.rustenburg_lm import RustenburgLmSource
    src = RustenburgLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
