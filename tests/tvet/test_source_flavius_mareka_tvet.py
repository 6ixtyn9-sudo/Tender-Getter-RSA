"""Tests for the Flavius Mareka TVET College tender source plug-in."""
import pytest


def test_flavius_mareka_tvet_source_initialization():
    from tender_getter.sources.tvet.flavius_mareka_tvet import FlaviusMarekaTvetSource
    src = FlaviusMarekaTvetSource()
    assert src.source_id == "flavius_mareka_tvet"
    assert src.live is True


def test_flavius_mareka_tvet_parse_mock_html():
    from tender_getter.sources.tvet.flavius_mareka_tvet import FlaviusMarekaTvetSource, MOCK_HTML
    src = FlaviusMarekaTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_flavius_mareka_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.flavius_mareka_tvet import FlaviusMarekaTvetSource
    src = FlaviusMarekaTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
