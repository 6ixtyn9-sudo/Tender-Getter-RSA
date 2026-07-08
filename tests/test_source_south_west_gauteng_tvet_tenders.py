"""Tests for the South West Gauteng TVET College tender source plug-in."""
import pytest


def test_south_west_gauteng_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.south_west_gauteng_tvet_tenders import SouthWestGautengTvetSource
    src = SouthWestGautengTvetSource()
    assert src.source_id == "south_west_gauteng_tvet_tenders"
    assert src.live is True


def test_south_west_gauteng_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.south_west_gauteng_tvet_tenders import SouthWestGautengTvetSource, MOCK_HTML
    src = SouthWestGautengTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_south_west_gauteng_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.south_west_gauteng_tvet_tenders import SouthWestGautengTvetSource
    src = SouthWestGautengTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
