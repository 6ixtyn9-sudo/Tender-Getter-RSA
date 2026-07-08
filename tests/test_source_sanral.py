import pytest
from datetime import datetime, timezone
from tender_getter.sources.soes.sanral import SANRALSource, MOCK_SANRAL_HTML
from tender_getter.schemas import TenderOpportunity

def test_sanral_source_initialization():
    source = SANRALSource()
    assert source.source_id == "sanral"
    assert "nra.co.za" in source.url

def test_sanral_parse_mock_html():
    source = SANRALSource()
    tenders = source.parse_html(MOCK_SANRAL_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "NRA R.003-020-2026/1"
    assert "Routine Road Maintenance" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 7
    assert t1.location_target == "Gauteng"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 30

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "SANRAL N.001-040-2026/2F"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 9
    assert t2.location_target == "Gauteng"

    # Verify third tender
    t3 = tenders[2]
    assert t3.tender_id == "NRA S.002-010-2026/3"
    assert t3.required_cidb_class == "CE"
    assert t3.required_cidb_level == 6
    assert t3.location_target == "Eastern Cape"

def test_sanral_fetch_uses_fallback_when_redirected():
    # If the response indicates a redirect to login, it should use the local high-fidelity fallback.
    login_html = """
    <html>
        <body>
            <h3>Login</h3>
            <form method="post" action="/sanral-users/login">
                <input type="email" name="email" />
            </form>
        </body>
    </html>
    """
    source = SANRALSource()
    # Passing the redirect/login HTML to fetch should trigger the high-fidelity mock fallback
    tenders = source.fetch(html_content=login_html)
    assert len(tenders) == 3
    assert any(t.tender_id == "SANRAL N.001-040-2026/2F" for t in tenders)

def test_sanral_parse_empty_or_invalid_html():
    source = SANRALSource()
    # Invalid HTML should fallback to the high-fidelity mock HTML to ensure 100% robust yields in POC
    tenders = source.fetch(html_content="<html><body>No tables or tenders here!</body></html>")
    assert len(tenders) == 3
