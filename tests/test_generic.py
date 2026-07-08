"""Tests for the generic parser utilities used by per-source plug-ins."""
import pytest
from tender_getter.sources.generic import standard_fetch, parse_html_table


def test_parse_html_table_basic():
    html = """
    <table>
      <tr><th>Ref</th><th>Description</th><th>Closing Date</th></tr>
      <tr><td>BID/2026/001</td><td>Some tender (Gauteng)</td><td>2026-09-01 11:00:00</td></tr>
    </table>
    """
    tenders = parse_html_table(html, issuing_entity="Test Entity")
    assert len(tenders) == 1
    assert tenders[0].tender_id == "BID/2026/001"
    assert tenders[0].issuing_entity == "Test Entity"
    assert tenders[0].location_target == "Gauteng"


def test_parse_html_table_with_cidb():
    html = """
    <table>
      <tr><td>CIDB/2026/001</td><td>Construction work Grade 4CE (Gauteng)</td><td>2026-09-01 11:00:00</td></tr>
    </table>
    """
    tenders = parse_html_table(html)
    assert len(tenders) == 1
    assert tenders[0].required_cidb_class == "CE"
    assert tenders[0].required_cidb_level == 4


def test_parse_html_table_respects_limit():
    html = """
    <table>
      <tr><td>A/001</td><td>First (Gauteng)</td><td>2026-09-01 11:00:00</td></tr>
      <tr><td>B/002</td><td>Second (Gauteng)</td><td>2026-09-02 11:00:00</td></tr>
      <tr><td>C/003</td><td>Third (Gauteng)</td><td>2026-09-03 11:00:00</td></tr>
    </table>
    """
    tenders = parse_html_table(html, limit=2)
    assert len(tenders) == 2


def test_parse_html_table_skips_headers():
    """Header rows have no digits in the ref column."""
    tenders = parse_html_table(
        "<table><tr><th>Ref</th><th>Description</th><th>Date</th></tr>"
        "<tr><td>BID/2026/001</td><td>Some tender (Gauteng)</td><td>2026-09-01 11:00:00</td></tr></table>"
    )
    assert len(tenders) == 1


def test_parse_html_table_handles_garbage():
    assert parse_html_table("<html><body>no tenders here</body></html>") == []


def test_standard_fetch_uses_mock_on_empty():
    tenders = standard_fetch(
        "https://example.invalid",
        "<table><tr><td>X/001</td><td>Test (Gauteng)</td><td>2026-09-01 11:00:00</td></tr></table>",
        html_content="<html>empty</html>",
    )
    assert len(tenders) == 1


def test_standard_fetch_falls_back_to_mock_on_invalid_url():
    """When live URL fails, fetch() should fall back to mock_html."""
    tenders = standard_fetch(
        "https://invalid.invalid.invalid",
        "<table><tr><td>X/001</td><td>Test (Gauteng)</td><td>2026-09-01 11:00:00</td></tr></table>",
    )
    assert len(tenders) == 1
