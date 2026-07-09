"""Tests for the per-source plug-in architecture + live-flag behaviour.

Architecture (v2.2.0): each entity has its own per-source Python file
under sources/<category>/<entity_id>.py with one TenderSource class.
Adding a new source = create one file + one test + one YAML entry.
"""
import pytest

from tender_getter.aggregator import (
    discover_source_classes,
    build_registry,
    get_all_source_instances,
)
from tender_getter.sources import load_sources


# ---------------------------------------------------------------------------
# Registry structure
# ---------------------------------------------------------------------------

def test_registry_covers_all_yaml_entries():
    """Every YAML entry must have a corresponding source class."""
    classes = discover_source_classes()
    class_ids = set(classes.keys())
    yaml_ids = {e["id"] for e in load_sources()}
    missing = yaml_ids - class_ids - {"etenders_csv", "etenders_ocds", "cidb_itender"}
    assert missing == set(), f"YAML entries without source classes: {sorted(missing)[:10]}"


def test_registry_has_at_least_700_classes():
    """We expect ~845 source classes."""
    classes = discover_source_classes()
    assert len(classes) >= 700, f"Only {len(classes)} source classes"


def test_registry_uniqueness_by_source_id():
    """Every source_id must be unique across all classes."""
    classes = discover_source_classes()
    ids = list(classes.keys())
    assert len(set(ids)) == len(ids), "Duplicate source_ids in registry"


def test_registry_classes_are_tender_sources():
    """Each class must conform to the TenderSource protocol."""
    from tender_getter.sources import TenderSource
    classes = discover_source_classes()
    for sid, cls in classes.items():
        assert hasattr(cls, "source_id"), f"{cls.__name__} missing source_id"
        assert callable(getattr(cls, "fetch", None)), f"{cls.__name__} missing fetch()"


# ---------------------------------------------------------------------------
# Live flag
# ---------------------------------------------------------------------------

def test_live_flag_in_yaml_for_all_entries():
    """Every YAML entry has an explicit `live:` field."""
    entries = load_sources()
    for e in entries:
        assert "live" in e, f"Missing 'live' for {e.get('id', 'unknown')}"


def test_live_count_is_honest():
    """At least 400 live=true, at least 200 live=false."""
    entries = load_sources()
    live_true = sum(1 for e in entries if e.get("live", True))
    live_false = sum(1 for e in entries if not e.get("live", True))
    assert live_true >= 100
    assert live_false >= 200


def test_live_only_filters_moribund_sources():
    """With live_only=True, YAML live=false sources are absent from registry."""
    yaml_entries = load_sources()
    moribund_ids = {e["id"] for e in yaml_entries if not e.get("live", True)}
    live_inst = get_all_source_instances(live_only=True)
    live_ids = {inst.source_id for inst in live_inst}
    overlap = moribund_ids & live_ids
    assert overlap == set(), f"Moribund sources leaked into live registry: {sorted(overlap)[:5]}"


def test_get_all_source_instances_default_includes_all():
    """By default, build_registry returns every class."""
    all_inst = get_all_source_instances(live_only=False)
    class_count = len(discover_source_classes())
    assert len(all_inst) == class_count


# ---------------------------------------------------------------------------
# Known sources
# ---------------------------------------------------------------------------

def test_denel_marked_moribund_in_yaml():
    """Denel is in business rescue."""
    yaml_map = {e["id"]: e for e in load_sources()}
    assert "denel" in yaml_map
    assert yaml_map["denel"]["live"] is False


def test_eskom_marked_live_in_yaml():
    yaml_map = {e["id"]: e for e in load_sources()}
    assert yaml_map["eskom"]["live"] is True


def test_armscor_in_registry():
    classes = discover_source_classes()
    assert "armscor" in classes


def test_setas_in_registry():
    """All 21 SETAs must be discoverable."""
    classes = discover_source_classes()
    seta_ids = {"agriseta", "bankseta", "ceta", "teta",
                "chieta", "hwseta", "services_seta", "wrseta"}
    assert seta_ids <= set(classes.keys())


def test_universities_in_registry():
    """Major universities must be discoverable."""
    classes = discover_source_classes()
    assert {"uct", "wits", "up", "ukzn", "uj"} <= set(classes.keys())


def test_water_board_consolidation_in_yaml():
    """Post-2026 mergers reflected in YAML."""
    yaml_map = {e["id"]: e for e in load_sources()}
    assert yaml_map["umngeni_uthukela_water"]["live"] is True
    assert yaml_map["vaal_central_water"]["live"] is True
    for legacy in ["umgeni_water", "mhlathuze_water"]:
        assert yaml_map[legacy]["live"] is False


def test_water_board_consolidation_in_registry():
    """The merged boards are discoverable as plug-ins."""
    classes = discover_source_classes()
    assert "umngeni_uthukela_water" in classes
    assert "vaal_central_water" in classes


# ---------------------------------------------------------------------------
# End-to-end (slow – skipped by default)
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_sync_all_sources_live_only_e2e():
    from tender_getter.aggregator import sync_all_sources
    summary = sync_all_sources(limit_per_source=0, verbose=False, live_only=True)
    assert summary["sources_total"] < summary["class_total"]
    assert summary["sources_skipped_live_false"] > 0
