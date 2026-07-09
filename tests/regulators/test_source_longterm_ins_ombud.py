"""Tests for the Ombudsman for Long-Term Insurance tender source plug-in."""
import pytest


def test_longterm_ins_ombud_source_initialization():
    from tender_getter.sources.regulators.longterm_ins_ombud import LongtermInsOmbudSource
    src = LongtermInsOmbudSource()
    assert src.source_id == "longterm_ins_ombud"
    assert src.live is True


def test_longterm_ins_ombud_parse_mock_html():
    from tender_getter.sources.regulators.longterm_ins_ombud import LongtermInsOmbudSource, MOCK_HTML
    src = LongtermInsOmbudSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_longterm_ins_ombud_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.longterm_ins_ombud import LongtermInsOmbudSource
    src = LongtermInsOmbudSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
