"""Tests for the Ubuntu (alt) tender source plug-in."""
import pytest


def test_ubuntu_lm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ubuntu_lm_alt_tenders import UbuntuLmAltSource
    src = UbuntuLmAltSource()
    assert src.source_id == "ubuntu_lm_alt_tenders"
    assert src.live is False


def test_ubuntu_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ubuntu_lm_alt_tenders import UbuntuLmAltSource, MOCK_HTML
    src = UbuntuLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ubuntu_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ubuntu_lm_alt_tenders import UbuntuLmAltSource
    src = UbuntuLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
