"""Tests for the Msunduzi Local Municipality (Pietermaritzburg) tender source plug-in."""
import pytest


def test_msunduzi_lm_source_initialization():
    from tender_getter.sources.local_municipalities.msunduzi_lm import MsunduziLmSource
    src = MsunduziLmSource()
    assert src.source_id == "msunduzi_lm"
    assert isinstance(src.live, bool)


def test_msunduzi_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.msunduzi_lm import MsunduziLmSource, MOCK_HTML
    src = MsunduziLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_msunduzi_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.msunduzi_lm import MsunduziLmSource
    src = MsunduziLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
