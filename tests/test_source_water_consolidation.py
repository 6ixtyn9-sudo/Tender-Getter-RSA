"""Tests for the post-2026 water board consolidation.

The 2026 DWS consolidation merged:
  - Umgeni + Mhlathuze -> uMngeni-uThukela Water
  - Bloem + Sedibeng + Lepelle -> Vaal Central Water

We document this in sources.yaml and verify the registry reflects the merger.
"""
import pytest
from tender_getter.sources import load_sources


def _yaml_map():
    return {e["id"]: e for e in load_sources()}


def test_merged_water_board_ids_present_in_yaml():
    """Both uMngeni-uThukela and Vaal Central Water must be in sources.yaml."""
    m = _yaml_map()
    assert "umngeni_uthukela_water_tenders" in m
    assert "vaal_central_water_tenders" in m


def test_merged_water_boards_marked_live():
    """Merged boards are the current active entities -> live=True."""
    m = _yaml_map()
    assert m["umngeni_uthukela_water_tenders"]["live"] is True
    assert m["vaal_central_water_tenders"]["live"] is True


def test_legacy_water_board_ids_marked_moribund():
    """Legacy boards (post-merger) are marked live=False in YAML."""
    m = _yaml_map()
    for legacy_id in [
        "umgeni_water_tenders", "mhlathuze_water_tenders",
        "bloem_water_tenders", "sedibeng_water_tenders", "lepelle_water_tenders",
    ]:
        assert legacy_id in m, f"Legacy {legacy_id} missing from registry"
        assert m[legacy_id]["live"] is False, f"{legacy_id} should be live=False (post-merger)"


def test_legacy_water_boards_excluded_under_live_only():
    """Legacy merged boards must be filtered out when live_only=True."""
    from tender_getter.aggregator import get_all_source_instances
    live_only = get_all_source_instances(live_only=True)
    live_only_ids = {inst.source_id for inst in live_only}
    for legacy_id in ["umgeni_water_tenders", "mhlathuze_water_tenders",
                      "bloem_water_tenders", "sedibeng_water_tenders", "lepelle_water_tenders"]:
        assert legacy_id not in live_only_ids, f"{legacy_id} should be excluded under live_only=True"
