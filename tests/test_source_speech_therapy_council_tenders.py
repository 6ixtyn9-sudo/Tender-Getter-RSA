"""Tests for the Speech Council tender source plug-in."""
import pytest


def test_speech_therapy_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.speech_therapy_council_tenders import SpeechTherapyCouncilSource
    src = SpeechTherapyCouncilSource()
    assert src.source_id == "speech_therapy_council_tenders"
    assert src.live is False


def test_speech_therapy_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.speech_therapy_council_tenders import SpeechTherapyCouncilSource, MOCK_HTML
    src = SpeechTherapyCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_speech_therapy_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.speech_therapy_council_tenders import SpeechTherapyCouncilSource
    src = SpeechTherapyCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
