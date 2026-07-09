"""Tests for the uMfolozi TVET College tender source plug-in."""
import pytest


def test_umfolozi_tvet_source_initialization():
    from tender_getter.sources.tvet.umfolozi_tvet import UmfoloziTvetSource
    src = UmfoloziTvetSource()
    assert src.source_id == "umfolozi_tvet"
    assert src.live is True


def test_umfolozi_tvet_parse_mock_html():
    from tender_getter.sources.tvet.umfolozi_tvet import UmfoloziTvetSource, MOCK_HTML
    src = UmfoloziTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umfolozi_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.umfolozi_tvet import UmfoloziTvetSource
    src = UmfoloziTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
