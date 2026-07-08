"""Tests for the Special Investigating Unit (SIU) tender source plug-in."""
import pytest


def test_siu_tenders_source_initialization():
    from tender_getter.sources.soes_extra.siu_tenders import SiuSource
    src = SiuSource()
    assert src.source_id == "siu_tenders"
    assert src.live is True


def test_siu_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.siu_tenders import SiuSource, MOCK_HTML
    src = SiuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_siu_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.siu_tenders import SiuSource
    src = SiuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
