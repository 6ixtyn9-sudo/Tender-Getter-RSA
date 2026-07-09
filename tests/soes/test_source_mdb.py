"""Tests for the Municipal Demarcation Board tender source plug-in."""
import pytest


def test_mdb_source_initialization():
    from tender_getter.sources.soes.mdb import MdbSource
    src = MdbSource()
    assert src.source_id == "mdb"
    assert isinstance(src.live, bool)


def test_mdb_parse_mock_html():
    from tender_getter.sources.soes.mdb import MdbSource, MOCK_HTML
    src = MdbSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mdb_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.mdb import MdbSource
    src = MdbSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
