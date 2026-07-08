"""Tests for the Albert Luthuli LM tender source plug-in."""
import pytest


def test_albert_luthuli_lm_source_initialization():
    from tender_getter.sources.local_municipalities.albert_luthuli_lm import AlbertLuthuliLmSource
    src = AlbertLuthuliLmSource()
    assert src.source_id == "albert_luthuli_lm"
    assert src.live is False


def test_albert_luthuli_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.albert_luthuli_lm import AlbertLuthuliLmSource, MOCK_HTML
    src = AlbertLuthuliLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_albert_luthuli_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.albert_luthuli_lm import AlbertLuthuliLmSource
    src = AlbertLuthuliLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
