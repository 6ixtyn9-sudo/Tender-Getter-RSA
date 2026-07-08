"""Tests for the Ombudsman for Long-Term Insurance tender source plug-in."""
import pytest


def test_longterm_ins_ombud_tenders_source_initialization():
    from tender_getter.sources.schedule3a.longterm_ins_ombud_tenders import LongtermInsOmbudSource
    src = LongtermInsOmbudSource()
    assert src.source_id == "longterm_ins_ombud_tenders"
    assert src.live is True


def test_longterm_ins_ombud_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.longterm_ins_ombud_tenders import LongtermInsOmbudSource, MOCK_HTML
    src = LongtermInsOmbudSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_longterm_ins_ombud_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.longterm_ins_ombud_tenders import LongtermInsOmbudSource
    src = LongtermInsOmbudSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
