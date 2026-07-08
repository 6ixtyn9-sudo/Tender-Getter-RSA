"""Tests for the Mmabatho LM tender source plug-in."""
import pytest


def test_mmabatho_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mmabatho_lm import MmabathoLmSource
    src = MmabathoLmSource()
    assert src.source_id == "mmabatho_lm"
    assert src.live is False


def test_mmabatho_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mmabatho_lm import MmabathoLmSource, MOCK_HTML
    src = MmabathoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mmabatho_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mmabatho_lm import MmabathoLmSource
    src = MmabathoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
