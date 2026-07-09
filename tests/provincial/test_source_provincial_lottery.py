"""Tests for the Provincial Lottery tender source plug-in."""
import pytest


def test_provincial_lottery_source_initialization():
    from tender_getter.sources.provincial.provincial_lottery import ProvincialLotterySource
    src = ProvincialLotterySource()
    assert src.source_id == "provincial_lottery"
    assert isinstance(src.live, bool)


def test_provincial_lottery_parse_mock_html():
    from tender_getter.sources.provincial.provincial_lottery import ProvincialLotterySource, MOCK_HTML
    src = ProvincialLotterySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_provincial_lottery_fetch_uses_fallback_on_empty():
    from tender_getter.sources.provincial.provincial_lottery import ProvincialLotterySource
    src = ProvincialLotterySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
