"""Tests for the Metsimaholo LM tender source plug-in."""
import pytest


def test_metsimaholo_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.metsimaholo_lm_tenders import MetsimaholoLmSource
    src = MetsimaholoLmSource()
    assert src.source_id == "metsimaholo_lm_tenders"
    assert src.live is False


def test_metsimaholo_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.metsimaholo_lm_tenders import MetsimaholoLmSource, MOCK_HTML
    src = MetsimaholoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_metsimaholo_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.metsimaholo_lm_tenders import MetsimaholoLmSource
    src = MetsimaholoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
