"""Tests for the Maluti TVET College tender source plug-in."""
import pytest


def test_maluti_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.maluti_tvet_tenders import MalutiTvetSource
    src = MalutiTvetSource()
    assert src.source_id == "maluti_tvet_tenders"
    assert src.live is True


def test_maluti_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.maluti_tvet_tenders import MalutiTvetSource, MOCK_HTML
    src = MalutiTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_maluti_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.maluti_tvet_tenders import MalutiTvetSource
    src = MalutiTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
