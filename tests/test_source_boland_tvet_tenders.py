"""Tests for the Boland TVET College tender source plug-in."""
import pytest


def test_boland_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.boland_tvet_tenders import BolandTvetSource
    src = BolandTvetSource()
    assert src.source_id == "boland_tvet_tenders"
    assert src.live is True


def test_boland_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.boland_tvet_tenders import BolandTvetSource, MOCK_HTML
    src = BolandTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_boland_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.boland_tvet_tenders import BolandTvetSource
    src = BolandTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
