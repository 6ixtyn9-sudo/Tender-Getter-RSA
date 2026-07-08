"""Tests for the Okhahlamba Local Municipality tender source plug-in."""
import pytest


def test_okhahlamba_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.okhahlamba_lm_tenders import OkhahlambaLmSource
    src = OkhahlambaLmSource()
    assert src.source_id == "okhahlamba_lm_tenders"
    assert src.live is True


def test_okhahlamba_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.okhahlamba_lm_tenders import OkhahlambaLmSource, MOCK_HTML
    src = OkhahlambaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_okhahlamba_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.okhahlamba_lm_tenders import OkhahlambaLmSource
    src = OkhahlambaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
