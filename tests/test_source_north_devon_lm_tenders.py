"""Tests for the North Devon LM tender source plug-in."""
import pytest


def test_north_devon_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.north_devon_lm_tenders import NorthDevonLmSource
    src = NorthDevonLmSource()
    assert src.source_id == "north_devon_lm_tenders"
    assert src.live is False


def test_north_devon_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.north_devon_lm_tenders import NorthDevonLmSource, MOCK_HTML
    src = NorthDevonLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_north_devon_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.north_devon_lm_tenders import NorthDevonLmSource
    src = NorthDevonLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
