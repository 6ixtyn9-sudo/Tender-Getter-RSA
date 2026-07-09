"""Tests for the uMhlabuyalingana LM tender source plug-in."""
import pytest


def test_umhlabuyalingana_lm_source_initialization():
    from tender_getter.sources.local_municipalities.umhlabuyalingana_lm import UmhlabuyalinganaLmSource
    src = UmhlabuyalinganaLmSource()
    assert src.source_id == "umhlabuyalingana_lm"
    assert src.live is False


def test_umhlabuyalingana_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.umhlabuyalingana_lm import UmhlabuyalinganaLmSource, MOCK_HTML
    src = UmhlabuyalinganaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umhlabuyalingana_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umhlabuyalingana_lm import UmhlabuyalinganaLmSource
    src = UmhlabuyalinganaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
