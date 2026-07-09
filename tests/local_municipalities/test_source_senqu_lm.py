"""Tests for the Senqu LM tender source plug-in."""
import pytest


def test_senqu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.senqu_lm import SenquLmSource
    src = SenquLmSource()
    assert src.source_id == "senqu_lm"
    assert isinstance(src.live, bool)


def test_senqu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.senqu_lm import SenquLmSource, MOCK_HTML
    src = SenquLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_senqu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.senqu_lm import SenquLmSource
    src = SenquLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
