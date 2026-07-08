"""Tests for the Psych Council tender source plug-in."""
import pytest


def test_psychology_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.psychology_council_tenders import PsychologyCouncilSource
    src = PsychologyCouncilSource()
    assert src.source_id == "psychology_council_tenders"
    assert src.live is False


def test_psychology_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.psychology_council_tenders import PsychologyCouncilSource, MOCK_HTML
    src = PsychologyCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_psychology_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.psychology_council_tenders import PsychologyCouncilSource
    src = PsychologyCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
