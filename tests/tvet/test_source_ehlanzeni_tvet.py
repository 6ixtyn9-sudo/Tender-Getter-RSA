"""Tests for the Ehlanzeni TVET College tender source plug-in."""
import pytest


def test_ehlanzeni_tvet_source_initialization():
    from tender_getter.sources.tvet.ehlanzeni_tvet import EhlanzeniTvetSource
    src = EhlanzeniTvetSource()
    assert src.source_id == "ehlanzeni_tvet"
    assert isinstance(src.live, bool)


def test_ehlanzeni_tvet_parse_mock_html():
    from tender_getter.sources.tvet.ehlanzeni_tvet import EhlanzeniTvetSource, MOCK_HTML
    src = EhlanzeniTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ehlanzeni_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.ehlanzeni_tvet import EhlanzeniTvetSource
    src = EhlanzeniTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
