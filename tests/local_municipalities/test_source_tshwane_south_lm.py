"""Tests for the Tshwane South LM tender source plug-in."""
import pytest


def test_tshwane_south_lm_source_initialization():
    from tender_getter.sources.local_municipalities.tshwane_south_lm import TshwaneSouthLmSource
    src = TshwaneSouthLmSource()
    assert src.source_id == "tshwane_south_lm"
    assert isinstance(src.live, bool)


def test_tshwane_south_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.tshwane_south_lm import TshwaneSouthLmSource, MOCK_HTML
    src = TshwaneSouthLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tshwane_south_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.tshwane_south_lm import TshwaneSouthLmSource
    src = TshwaneSouthLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
