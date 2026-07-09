"""Tests for the Sedibeng TVET College tender source plug-in."""
import pytest


def test_sedibeng_tvet_source_initialization():
    from tender_getter.sources.tvet.sedibeng_tvet import SedibengTvetSource
    src = SedibengTvetSource()
    assert src.source_id == "sedibeng_tvet"
    assert src.live is True


def test_sedibeng_tvet_parse_mock_html():
    from tender_getter.sources.tvet.sedibeng_tvet import SedibengTvetSource, MOCK_HTML
    src = SedibengTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sedibeng_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.sedibeng_tvet import SedibengTvetSource
    src = SedibengTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
