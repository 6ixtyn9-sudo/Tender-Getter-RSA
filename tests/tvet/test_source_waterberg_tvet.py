"""Tests for the Waterberg TVET College tender source plug-in."""
import pytest


def test_waterberg_tvet_source_initialization():
    from tender_getter.sources.tvet.waterberg_tvet import WaterbergTvetSource
    src = WaterbergTvetSource()
    assert src.source_id == "waterberg_tvet"
    assert isinstance(src.live, bool)


def test_waterberg_tvet_parse_mock_html():
    from tender_getter.sources.tvet.waterberg_tvet import WaterbergTvetSource, MOCK_HTML
    src = WaterbergTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_waterberg_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.waterberg_tvet import WaterbergTvetSource
    src = WaterbergTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
