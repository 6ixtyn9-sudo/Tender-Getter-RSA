"""Tests for the Mining Qualifications Authority (MQA) tender source plug-in."""
import pytest


def test_mqa_tenders_source_initialization():
    from tender_getter.sources.setas.mqa_tenders import MqaSource
    src = MqaSource()
    assert src.source_id == "mqa_tenders"
    assert src.live is True


def test_mqa_tenders_parse_mock_html():
    from tender_getter.sources.setas.mqa_tenders import MqaSource, MOCK_HTML
    src = MqaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mqa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.mqa_tenders import MqaSource
    src = MqaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
