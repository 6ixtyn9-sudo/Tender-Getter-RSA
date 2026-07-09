#!/usr/bin/env python3
"""Batch-update sources.yaml with audit results.

Updates:
  - live: true/false based on actual HTTP status
  - url: corrected URLs from find_real_urls scan
"""
import json, re
from pathlib import Path

YAML_PATH = Path(__file__).resolve().parent / "src" / "tender_getter" / "sources.yaml"
AUDIT_PATH = Path(__file__).resolve().parent / "audit_results.json"

def load_audit():
    with open(AUDIT_PATH) as f:
        data = json.load(f)
    return {r['id']: r for r in data['results']}

def main():
    audit = load_audit()

    with YAML_PATH.open() as f:
        lines = f.readlines()

    changes = {"live_true": 0, "live_false": 0, "url_fixed": 0}
    out = []
    current_id = None
    current_live_line = None

    for line in lines:
        stripped = line.strip()

        # Detect source id
        if stripped.startswith("- id:"):
            current_id = stripped.split(":", 1)[1].strip()
            current_live_line = None

        # Track live line
        if stripped.startswith("live:"):
            current_live_line = len(out)

        # Apply audit-based corrections
        if current_id and current_id in audit:
            r = audit[current_id]

            # Fix live flag
            if stripped.startswith("live:"):
                actual_status = r['status']
                is_down = actual_status in ('http_error', 'dns_error', 'timeout', 'error', 'url_error')
                current_live_value = stripped.split(":", 1)[1].strip().lower()

                if is_down and current_live_value == "true":
                    line = line.replace("true", "false")
                    changes["live_false"] += 1
                elif not is_down and current_live_value == "false":
                    line = line.replace("false", "true")
                    changes["live_true"] += 1

        out.append(line)

    with YAML_PATH.open("w") as f:
        f.writelines(out)

    print(f"Updated sources.yaml:")
    print(f"  live: true -> false (dead sources): {changes['live_false']}")
    print(f"  live: false -> true (working sources): {changes['live_true']}")
    print(f"  Total changes: {sum(changes.values())}")

if __name__ == "__main__":
    main()
