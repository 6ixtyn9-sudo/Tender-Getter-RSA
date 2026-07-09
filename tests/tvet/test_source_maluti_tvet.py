"""Tests for the Maluti TVET College tender source plug-in."""
import pytest


def test_maluti_tvet_source_initialization():
    from tender_getter.sources.tvet.maluti_tvet import MalutiTvetSource
    src = MalutiTvetSource()
    assert src.source_id == "maluti_tvet"
    assert isinstance(src.live, bool)


def test_maluti_tvet_parse_mock_html():
    from tender_getter.sources.tvet.maluti_tvet import MalutiTvetSource, MOCK_HTML
    src = MalutiTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_maluti_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.maluti_tvet import MalutiTvetSource
    src = MalutiTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
