"""Tests for the Central Johannesburg TVET College tender source plug-in."""
import pytest


def test_central_johannesburg_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.central_johannesburg_tvet_tenders import CentralJohannesburgTvetSource
    src = CentralJohannesburgTvetSource()
    assert src.source_id == "central_johannesburg_tvet_tenders"
    assert src.live is True


def test_central_johannesburg_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.central_johannesburg_tvet_tenders import CentralJohannesburgTvetSource, MOCK_HTML
    src = CentralJohannesburgTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_central_johannesburg_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.central_johannesburg_tvet_tenders import CentralJohannesburgTvetSource
    src = CentralJohannesburgTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
