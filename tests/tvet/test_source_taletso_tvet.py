"""Tests for the Taletso TVET College tender source plug-in."""
import pytest


def test_taletso_tvet_source_initialization():
    from tender_getter.sources.tvet.taletso_tvet import TaletsoTvetSource
    src = TaletsoTvetSource()
    assert src.source_id == "taletso_tvet"
    assert src.live is True


def test_taletso_tvet_parse_mock_html():
    from tender_getter.sources.tvet.taletso_tvet import TaletsoTvetSource, MOCK_HTML
    src = TaletsoTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_taletso_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.taletso_tvet import TaletsoTvetSource
    src = TaletsoTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
