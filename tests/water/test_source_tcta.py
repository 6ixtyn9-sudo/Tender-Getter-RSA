import pytest
from tender_getter.sources.water.tcta import TctaSource

def test_tcta_source_initialization():
    source = TctaSource()
    assert source.source_id == "tcta"
    assert source.url.startswith("http")


