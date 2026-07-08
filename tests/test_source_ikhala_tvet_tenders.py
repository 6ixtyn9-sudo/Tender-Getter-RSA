"""Tests for the Ikhala TVET College tender source plug-in."""
import pytest


def test_ikhala_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.ikhala_tvet_tenders import IkhalaTvetSource
    src = IkhalaTvetSource()
    assert src.source_id == "ikhala_tvet_tenders"
    assert src.live is True


def test_ikhala_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.ikhala_tvet_tenders import IkhalaTvetSource, MOCK_HTML
    src = IkhalaTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ikhala_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.ikhala_tvet_tenders import IkhalaTvetSource
    src = IkhalaTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
