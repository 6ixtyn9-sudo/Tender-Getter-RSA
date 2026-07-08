"""Tests for the Govan Mbeki (alt) tender source plug-in."""
import pytest


def test_govan_mbeki_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.govan_mbeki_alt_tenders import GovanMbekiAltSource
    src = GovanMbekiAltSource()
    assert src.source_id == "govan_mbeki_alt_tenders"
    assert src.live is True


def test_govan_mbeki_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.govan_mbeki_alt_tenders import GovanMbekiAltSource, MOCK_HTML
    src = GovanMbekiAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_govan_mbeki_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.govan_mbeki_alt_tenders import GovanMbekiAltSource
    src = GovanMbekiAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
