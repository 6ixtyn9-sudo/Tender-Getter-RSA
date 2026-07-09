"""Tests for the Eastcape Midlands TVET College tender source plug-in."""
import pytest


def test_eastcape_midlands_tvet_source_initialization():
    from tender_getter.sources.tvet.eastcape_midlands_tvet import EastcapeMidlandsTvetSource
    src = EastcapeMidlandsTvetSource()
    assert src.source_id == "eastcape_midlands_tvet"
    assert isinstance(src.live, bool)


def test_eastcape_midlands_tvet_parse_mock_html():
    from tender_getter.sources.tvet.eastcape_midlands_tvet import EastcapeMidlandsTvetSource, MOCK_HTML
    src = EastcapeMidlandsTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eastcape_midlands_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.eastcape_midlands_tvet import EastcapeMidlandsTvetSource
    src = EastcapeMidlandsTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
