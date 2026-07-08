"""Tests for the Inxuba Yethemba LM tender source plug-in."""
import pytest


def test_inxuba_yethemba_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.inxuba_yethemba_lm_tenders import InxubaYethembaLmSource
    src = InxubaYethembaLmSource()
    assert src.source_id == "inxuba_yethemba_lm_tenders"
    assert src.live is False


def test_inxuba_yethemba_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.inxuba_yethemba_lm_tenders import InxubaYethembaLmSource, MOCK_HTML
    src = InxubaYethembaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_inxuba_yethemba_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.inxuba_yethemba_lm_tenders import InxubaYethembaLmSource
    src = InxubaYethembaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
