import pytest
from tender_getter.sources.metros.johannesburg import JohannesburgSource

def test_johannesburg_source_initialization():
    source = JohannesburgSource()
    assert source.source_id == "johannesburg"
    assert source.url.startswith("http")
