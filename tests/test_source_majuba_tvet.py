"""Tests for the Majuba TVET College tender source plug-in."""
import pytest


def test_majuba_tvet_source_initialization():
    from tender_getter.sources.tvet.majuba_tvet import MajubaTvetSource
    src = MajubaTvetSource()
    assert src.source_id == "majuba_tvet"
    assert src.live is True


def test_majuba_tvet_parse_mock_html():
    from tender_getter.sources.tvet.majuba_tvet import MajubaTvetSource, MOCK_HTML
    src = MajubaTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_majuba_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.majuba_tvet import MajubaTvetSource
    src = MajubaTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
