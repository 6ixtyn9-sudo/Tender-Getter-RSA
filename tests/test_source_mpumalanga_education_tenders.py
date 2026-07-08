"""Tests for the Mpumalanga Department of Education tender source plug-in."""
import pytest


def test_mpumalanga_education_tenders_source_initialization():
    from tender_getter.sources.research_extra.mpumalanga_education_tenders import MpumalangaEducationSource
    src = MpumalangaEducationSource()
    assert src.source_id == "mpumalanga_education_tenders"
    assert src.live is True


def test_mpumalanga_education_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mpumalanga_education_tenders import MpumalangaEducationSource, MOCK_HTML
    src = MpumalangaEducationSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mpumalanga_education_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mpumalanga_education_tenders import MpumalangaEducationSource
    src = MpumalangaEducationSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
