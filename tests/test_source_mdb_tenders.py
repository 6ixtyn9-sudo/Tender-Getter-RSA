"""Tests for the Municipal Demarcation Board tender source plug-in."""
import pytest


def test_mdb_tenders_source_initialization():
    from tender_getter.sources.soes_extra.mdb_tenders import MdbSource
    src = MdbSource()
    assert src.source_id == "mdb_tenders"
    assert src.live is True


def test_mdb_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.mdb_tenders import MdbSource, MOCK_HTML
    src = MdbSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mdb_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.mdb_tenders import MdbSource
    src = MdbSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
