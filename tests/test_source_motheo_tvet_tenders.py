"""Tests for the Motheo TVET College tender source plug-in."""
import pytest


def test_motheo_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.motheo_tvet_tenders import MotheoTvetSource
    src = MotheoTvetSource()
    assert src.source_id == "motheo_tvet_tenders"
    assert src.live is True


def test_motheo_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.motheo_tvet_tenders import MotheoTvetSource, MOCK_HTML
    src = MotheoTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_motheo_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.motheo_tvet_tenders import MotheoTvetSource
    src = MotheoTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
