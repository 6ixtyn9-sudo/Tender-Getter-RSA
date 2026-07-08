"""Tests for the Taletso TVET College tender source plug-in."""
import pytest


def test_taletso_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.taletso_tvet_tenders import TaletsoTvetSource
    src = TaletsoTvetSource()
    assert src.source_id == "taletso_tvet_tenders"
    assert src.live is True


def test_taletso_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.taletso_tvet_tenders import TaletsoTvetSource, MOCK_HTML
    src = TaletsoTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_taletso_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.taletso_tvet_tenders import TaletsoTvetSource
    src = TaletsoTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
