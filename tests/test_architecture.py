import os
from pathlib import Path
import yaml

def test_yaml_entries_match_python_files():
    """Asserts that len(yaml_entries) == len(py_files)."""
    src_dir = Path("src/tender_getter/sources")
    
    # Load YAML
    yaml_file = Path("src/tender_getter/sources.yaml")
    assert yaml_file.exists(), "sources.yaml is missing"
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
    yaml_entries = data.get("sources", [])
    
    # Count Python files
    py_files = [f for f in src_dir.rglob("*.py") if f.name not in ["__init__.py", "generic.py", "common.py", "etenders_ocds.py", "etenders_csv.py", "cidb_itender.py"]]
    
    # Some bespoke files may not have matching YAML entry if they're not in the main loop, 
    # but the rule says the file tree is the source of truth, so len should match.
    assert len(yaml_entries) == len(py_files), f"YAML has {len(yaml_entries)} entries, but {len(py_files)} Python source files found."

def test_west_rand_is_exactly_one_file():
    """Asserts that there is exactly ONE file for west_rand, in districts/."""
    src_dir = Path("src/tender_getter/sources")
    matches = list(src_dir.rglob("west_rand*.py"))
    assert len(matches) == 1, f"Expected exactly 1 west_rand file, found {len(matches)}: {matches}"
    assert matches[0].parent.name == "districts", f"west_rand file should be in districts/, but is in {matches[0].parent.name}"

def test_acsa_is_exactly_one_file():
    """Asserts that there is exactly ONE file for acsa, in soes/."""
    src_dir = Path("src/tender_getter/sources")
    matches = list(src_dir.rglob("acsa*.py"))
    assert len(matches) == 1, f"Expected exactly 1 acsa file, found {len(matches)}: {matches}"
    assert matches[0].parent.name == "soes", f"acsa file should be in soes/, but is in {matches[0].parent.name}"
