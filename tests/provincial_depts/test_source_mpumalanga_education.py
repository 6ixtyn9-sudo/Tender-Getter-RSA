import pytest
from tender_getter.sources.provincial_depts.mpumalanga_education import MpumalangaEducationSource, MOCK_MPUMALANGA_EDUCATION_HTML
def test_mpumalanga_education_source_initialization():
    source = MpumalangaEducationSource()
    assert source.source_id == "mpumalanga_education"
    assert source.url.startswith("http")
def test_mpumalanga_education_parse_mock_html():
    source = MpumalangaEducationSource()
    tenders = source.parse_html(MOCK_MPUMALANGA_EDUCATION_HTML)
    assert len(tenders) == 3
def test_mpumalanga_education_fetch_uses_fallback_on_empty_or_error():
    source = MpumalangaEducationSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
