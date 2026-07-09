"""Tests for the Dipaleseng Local Municipality tender source plug-in."""
import pytest


def test_dipaleseng_lm_source_initialization():
    from tender_getter.sources.local_municipalities.dipaleseng_lm import DipalesengLmSource
    src = DipalesengLmSource()
    assert src.source_id == "dipaleseng_lm"
    assert isinstance(src.live, bool)


def test_dipaleseng_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.dipaleseng_lm import DipalesengLmSource, MOCK_HTML
    src = DipalesengLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dipaleseng_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.dipaleseng_lm import DipalesengLmSource
    src = DipalesengLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
