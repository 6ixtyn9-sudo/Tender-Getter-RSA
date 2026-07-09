"""Tests for the Mantsopa LM tender source plug-in."""
import pytest


def test_mantsopa_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mantsopa_lm import MantsopaLmSource
    src = MantsopaLmSource()
    assert src.source_id == "mantsopa_lm"
    assert src.live is True


def test_mantsopa_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mantsopa_lm import MantsopaLmSource, MOCK_HTML
    src = MantsopaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mantsopa_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mantsopa_lm import MantsopaLmSource
    src = MantsopaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
