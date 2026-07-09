"""Tests for the Speech Council tender source plug-in."""
import pytest


def test_speech_therapy_council_source_initialization():
    from tender_getter.sources.research.speech_therapy_council import SpeechTherapyCouncilSource
    src = SpeechTherapyCouncilSource()
    assert src.source_id == "speech_therapy_council"
    assert isinstance(src.live, bool)


def test_speech_therapy_council_parse_mock_html():
    from tender_getter.sources.research.speech_therapy_council import SpeechTherapyCouncilSource, MOCK_HTML
    src = SpeechTherapyCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_speech_therapy_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.speech_therapy_council import SpeechTherapyCouncilSource
    src = SpeechTherapyCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
