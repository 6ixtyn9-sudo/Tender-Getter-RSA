"""Tests for the Ingwe TVET College tender source plug-in."""
import pytest


def test_ingwe_tvet_source_initialization():
    from tender_getter.sources.tvet.ingwe_tvet import IngweTvetSource
    src = IngweTvetSource()
    assert src.source_id == "ingwe_tvet"
    assert src.live is True


def test_ingwe_tvet_parse_mock_html():
    from tender_getter.sources.tvet.ingwe_tvet import IngweTvetSource, MOCK_HTML
    src = IngweTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ingwe_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.ingwe_tvet import IngweTvetSource
    src = IngweTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
