"""Tests for the Elangeni TVET College tender source plug-in."""
import pytest


def test_elangeni_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.elangeni_tvet_tenders import ElangeniTvetSource
    src = ElangeniTvetSource()
    assert src.source_id == "elangeni_tvet_tenders"
    assert src.live is True


def test_elangeni_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.elangeni_tvet_tenders import ElangeniTvetSource, MOCK_HTML
    src = ElangeniTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_elangeni_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.elangeni_tvet_tenders import ElangeniTvetSource
    src = ElangeniTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
