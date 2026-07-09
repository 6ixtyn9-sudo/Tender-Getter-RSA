"""Tests for the Media, Information and Communication Technologies SETA (MICT SETA) tender source plug-in."""
import pytest


def test_mict_seta_source_initialization():
    from tender_getter.sources.setas.mict_seta import MictSetaSource
    src = MictSetaSource()
    assert src.source_id == "mict_seta"
    assert isinstance(src.live, bool)


def test_mict_seta_parse_mock_html():
    from tender_getter.sources.setas.mict_seta import MictSetaSource, MOCK_HTML
    src = MictSetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mict_seta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.mict_seta import MictSetaSource
    src = MictSetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
