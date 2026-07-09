"""Tests for the Phalaborwa LM tender source plug-in."""
import pytest


def test_phalaborwa_lm_source_initialization():
    from tender_getter.sources.local_municipalities.phalaborwa_lm import PhalaborwaLmSource
    src = PhalaborwaLmSource()
    assert src.source_id == "phalaborwa_lm"
    assert isinstance(src.live, bool)


def test_phalaborwa_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.phalaborwa_lm import PhalaborwaLmSource, MOCK_HTML
    src = PhalaborwaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_phalaborwa_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.phalaborwa_lm import PhalaborwaLmSource
    src = PhalaborwaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
