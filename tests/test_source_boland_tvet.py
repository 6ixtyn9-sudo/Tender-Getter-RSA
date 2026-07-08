"""Tests for the Boland TVET College tender source plug-in."""
import pytest


def test_boland_tvet_source_initialization():
    from tender_getter.sources.tvet.boland_tvet import BolandTvetSource
    src = BolandTvetSource()
    assert src.source_id == "boland_tvet"
    assert src.live is True


def test_boland_tvet_parse_mock_html():
    from tender_getter.sources.tvet.boland_tvet import BolandTvetSource, MOCK_HTML
    src = BolandTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_boland_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.boland_tvet import BolandTvetSource
    src = BolandTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
