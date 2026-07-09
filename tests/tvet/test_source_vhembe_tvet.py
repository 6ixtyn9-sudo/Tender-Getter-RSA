"""Tests for the Vhembe TVET College tender source plug-in."""
import pytest


def test_vhembe_tvet_source_initialization():
    from tender_getter.sources.tvet.vhembe_tvet import VhembeTvetSource
    src = VhembeTvetSource()
    assert src.source_id == "vhembe_tvet"
    assert isinstance(src.live, bool)


def test_vhembe_tvet_parse_mock_html():
    from tender_getter.sources.tvet.vhembe_tvet import VhembeTvetSource, MOCK_HTML
    src = VhembeTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_vhembe_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.vhembe_tvet import VhembeTvetSource
    src = VhembeTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
