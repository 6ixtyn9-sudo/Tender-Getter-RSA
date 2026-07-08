"""Tests for the Ubuntu LM tender source plug-in."""
import pytest


def test_ubuntu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.ubuntu_lm import UbuntuLmSource
    src = UbuntuLmSource()
    assert src.source_id == "ubuntu_lm"
    assert src.live is False


def test_ubuntu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.ubuntu_lm import UbuntuLmSource, MOCK_HTML
    src = UbuntuLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ubuntu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ubuntu_lm import UbuntuLmSource
    src = UbuntuLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
