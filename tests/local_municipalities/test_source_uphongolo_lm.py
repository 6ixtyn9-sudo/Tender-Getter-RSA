"""Tests for the uPhongolo LM tender source plug-in."""
import pytest


def test_uphongolo_lm_source_initialization():
    from tender_getter.sources.local_municipalities.uphongolo_lm import UphongoloLmSource
    src = UphongoloLmSource()
    assert src.source_id == "uphongolo_lm"
    assert src.live is False


def test_uphongolo_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.uphongolo_lm import UphongoloLmSource, MOCK_HTML
    src = UphongoloLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uphongolo_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.uphongolo_lm import UphongoloLmSource
    src = UphongoloLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
