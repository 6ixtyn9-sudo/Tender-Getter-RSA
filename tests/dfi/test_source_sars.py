import pytest
from tender_getter.sources.dfi.sars import SarsSource

def test_sars_source_initialization():
    source = SarsSource()
    assert source.source_id == "sars"
    assert source.url.startswith("http")


