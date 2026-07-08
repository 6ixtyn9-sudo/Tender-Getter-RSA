"""Tests for the Maquassi Hills Local Municipality tender source plug-in."""
import pytest


def test_maquassi_hills_lm_source_initialization():
    from tender_getter.sources.local_municipalities.maquassi_hills_lm import MaquassiHillsLmSource
    src = MaquassiHillsLmSource()
    assert src.source_id == "maquassi_hills_lm"
    assert src.live is True


def test_maquassi_hills_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.maquassi_hills_lm import MaquassiHillsLmSource, MOCK_HTML
    src = MaquassiHillsLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_maquassi_hills_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.maquassi_hills_lm import MaquassiHillsLmSource
    src = MaquassiHillsLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
