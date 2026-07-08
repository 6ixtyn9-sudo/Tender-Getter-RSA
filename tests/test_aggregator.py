import pytest
from tender_getter.aggregator import discover_source_classes, get_all_source_instances, sync_all_sources

def test_discover_finds_many_sources():
    classes = discover_source_classes()
    # We expect at least 100 source classes (full registry is 112+)
    assert len(classes) >= 100
    # Check a few known ones are present
    ids = {getattr(c, "source_id", "") for c in classes}
    assert "johannesburg_tenders" in ids
    assert "capetown_tenders" in ids
    assert "eskom" in ids or "eskom" in str(ids).lower() or any("eskom" in s for s in ids)
    # check at least one from each major category
    assert any("gauteng" in s for s in ids)
    assert any("water" in s for s in ids)
    assert any("saps" in s or "prasa" in s for s in ids)

def test_sync_all_runs_with_limit():
    summary = sync_all_sources(limit_per_source=1, verbose=False)
    assert summary["sources_total"] >= 100
    assert summary["sources_ok"] >= summary["sources_total"] * 0.9  # allow <10% failures
    assert summary["tenders_unique"] >= 50
    assert summary["tenders_upserted"] >= 50
