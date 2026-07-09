"""Tests for the Manteng LM tender source plug-in."""
import pytest


def test_manteng_lm_source_initialization():
    from tender_getter.sources.local_municipalities.manteng_lm import MantengLmSource
    src = MantengLmSource()
    assert src.source_id == "manteng_lm"
    assert src.live is False


def test_manteng_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.manteng_lm import MantengLmSource, MOCK_HTML
    src = MantengLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_manteng_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.manteng_lm import MantengLmSource
    src = MantengLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
