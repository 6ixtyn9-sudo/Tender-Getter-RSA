"""Tests for the Sakhisizwe LM tender source plug-in."""
import pytest


def test_sakhisizwe_lm_source_initialization():
    from tender_getter.sources.local_municipalities.sakhisizwe_lm import SakhisizweLmSource
    src = SakhisizweLmSource()
    assert src.source_id == "sakhisizwe_lm"
    assert src.live is False


def test_sakhisizwe_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.sakhisizwe_lm import SakhisizweLmSource, MOCK_HTML
    src = SakhisizweLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sakhisizwe_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.sakhisizwe_lm import SakhisizweLmSource
    src = SakhisizweLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
