"""Tests for the Okhahlamba (alt) tender source plug-in."""
import pytest


def test_okhahlamba_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.okhahlamba_lm_alt_tenders import OkhahlambaLmAltSource
    src = OkhahlambaLmAltSource()
    assert src.source_id == "okhahlamba_lm_alt_tenders"
    assert src.live is False


def test_okhahlamba_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.okhahlamba_lm_alt_tenders import OkhahlambaLmAltSource, MOCK_HTML
    src = OkhahlambaLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_okhahlamba_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.okhahlamba_lm_alt_tenders import OkhahlambaLmAltSource
    src = OkhahlambaLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
