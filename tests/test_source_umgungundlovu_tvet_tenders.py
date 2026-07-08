"""Tests for the uMgungundlovu TVET College tender source plug-in."""
import pytest


def test_umgungundlovu_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.umgungundlovu_tvet_tenders import UmgungundlovuTvetSource
    src = UmgungundlovuTvetSource()
    assert src.source_id == "umgungundlovu_tvet_tenders"
    assert src.live is True


def test_umgungundlovu_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.umgungundlovu_tvet_tenders import UmgungundlovuTvetSource, MOCK_HTML
    src = UmgungundlovuTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umgungundlovu_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.umgungundlovu_tvet_tenders import UmgungundlovuTvetSource
    src = UmgungundlovuTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
