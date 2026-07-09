"""Tests for the Independent Electoral Commission (IEC) tender source plug-in."""
import pytest


def test_iec_source_initialization():
    from tender_getter.sources.soes.iec import IecSource
    src = IecSource()
    assert src.source_id == "iec"
    assert isinstance(src.live, bool)


def test_iec_parse_mock_html():
    from tender_getter.sources.soes.iec import IecSource, MOCK_HTML
    src = IecSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_iec_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.iec import IecSource
    src = IecSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
