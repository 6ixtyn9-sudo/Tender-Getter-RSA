"""Tests for the Sekhukhune TVET College tender source plug-in."""
import pytest


def test_sekhukhune_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.sekhukhune_tvet_tenders import SekhukhuneTvetSource
    src = SekhukhuneTvetSource()
    assert src.source_id == "sekhukhune_tvet_tenders"
    assert src.live is True


def test_sekhukhune_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.sekhukhune_tvet_tenders import SekhukhuneTvetSource, MOCK_HTML
    src = SekhukhuneTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sekhukhune_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.sekhukhune_tvet_tenders import SekhukhuneTvetSource
    src = SekhukhuneTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
