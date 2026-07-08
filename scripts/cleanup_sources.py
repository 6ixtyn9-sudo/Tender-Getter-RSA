import re
import yaml
from pathlib import Path
from collections import defaultdict
import os
import shutil

source_dir = Path("src/tender_getter/sources")
tests_dir = Path("tests")

all_files = list(source_dir.rglob("*.py"))
files = [f for f in all_files if f.name != "__init__.py" and f.name != "generic.py" and f.name != "common.py"]

# 1. Identify alt files
alt_files = [f for f in files if "_alt_tenders.py" in f.name or "_alt_2_tenders.py" in f.name]

# 2. Identify duplicates
base_to_files = defaultdict(list)
for f in files:
    if f in alt_files: continue
    
    txt = f.read_text()
    m = re.search(r'source_id:\s*str\s*=\s*"([^"]+)"', txt)
    if m:
        sid = m.group(1)
        base_to_files[sid].append(f)
    else:
        name = f.stem
        if name.endswith("_tenders"):
            base_name = name[:-8]
            base_to_files[base_name].append(f)
        else:
            base_to_files[name].append(f)

duplicates_to_delete = []
keep_files = []

for base, fs in base_to_files.items():
    if len(fs) > 1:
        # Prefer the one that does NOT end in _tenders in filename
        fs.sort(key=lambda x: (not x.stem.endswith("_tenders"), len(x.read_text())), reverse=True)
        keep_files.append(fs[0])
        duplicates_to_delete.extend(fs[1:])
    else:
        keep_files.append(fs[0])

# Perform Deletions
deleted_count = 0
for f in alt_files + duplicates_to_delete:
    test_file = tests_dir / f"test_source_{f.stem}.py"
    if f.exists():
        f.unlink()
        deleted_count += 1
    if test_file.exists():
        test_file.unlink()
        deleted_count += 1

print(f"Deleted {deleted_count} source and test files.")

# 3. Categorize remaining keep_files
def assign_cat(f):
    name = f.stem
    if "_lm_" in name or "local_municipality" in name: return "local_municipalities"
    if "_dm_" in name or "district_municipality" in name: return "districts"
    if "tvet" in name: return "tvet"
    if "seta" in name: return "setas"
    if "university" in name or "univ" in name or name in ['uct_tenders', 'wits_tenders', 'up_tenders', 'smu_health_tenders']: return "universities"
    if "water" in name: return "water"
    if "soe" in name or name in ['eskom', 'transnet', 'sanral', 'sita', 'sabc', 'acsa_tenders', 'prasa', 'denel']: return "soes"
    if name in ['saps', 'dha', 'dhs', 'dws', 'dpwi', 'dffe', 'dod']: return "national_depts"
    if "provincial" in name or "wc_" in name or "gauteng_" in name: return "provincial"
    if "metro" in name or name in ['capetown', 'johannesburg', 'ethekwini', 'tshwane', 'ekurhuleni', 'nelson_mandela_bay', 'mangaung', 'buffalo_city']: return "metros"
    
    # regulators logic
    if name in ['nersa_tenders', 'nnr_tenders', 'ppra_tenders', 'fsca_tenders']: return "regulators"
    
    if f.parent.name in ['research_extra', 'soes_extra', 'districts_full', 'schedule3a']:
        # if it's in schedule3a, maybe it should be a regulator or stay in schedule3a? 
        # The user said "schedule3a ... most should go to dfi/, research/, or a new regulators/ directory"
        # Let's map any remaining schedule3a to regulators if we can't tell, or just keep schedule3a for the rest
        if 'research' in name or 'council' in name or 'institute' in name or 'museum' in name or 'heritage' in name or 'nrf' in name:
            return 'research'
        if 'regulator' in name or 'authority' in name or 'board' in name or 'commission' in name or 'agency' in name or 'fund' in name or 'ombud' in name:
            return 'regulators'
        if f.parent.name == 'schedule3a':
            return 'schedule3a'
        if f.parent.name == 'research_extra':
            return 'research'
        if f.parent.name == 'soes_extra':
            return 'soes'
        if f.parent.name == 'districts_full':
            return 'districts'
            
    return f.parent.name

moved_count = 0
for f in keep_files:
    target_cat = assign_cat(f)
    if f.parent.name != target_cat:
        target_dir = source_dir / target_cat
        target_dir.mkdir(exist_ok=True)
        shutil.move(str(f), str(target_dir / f.name))
        moved_count += 1

print(f"Moved {moved_count} source files.")

# Clean up empty dirs
for d in ['research_extra', 'soes_extra', 'districts_full']:
    d_path = source_dir / d
    if d_path.exists() and not any(d_path.iterdir()):
        d_path.rmdir()

# 4. Regenerate YAML
yaml_entries = []
for f in source_dir.rglob("*.py"):
    if f.name in ["__init__.py", "generic.py", "common.py", "etenders_ocds.py", "etenders_csv.py", "cidb_itender.py"]:
        continue
    txt = f.read_text()
    m = re.search(r'source_id:\s*str\s*=\s*"([^"]+)"', txt)
    if m:
        sid = m.group(1)
        name_match = re.search(r'name:\s*str\s*=\s*"([^"]+)"', txt)
        name = name_match.group(1) if name_match else sid.replace("_tenders", "").replace("_", " ").title()
        
        live_match = re.search(r'live\s*=\s*(True|False)', txt)
        live = True
        if live_match:
            live = live_match.group(1) == 'True'
            
        yaml_entries.append({
            'id': sid,
            'name': name,
            'live': live
        })
    else:
        # For bespoke ones like capetown.py which inherit from TenderSource
        # wait, all of them should have source_id
        pass

yaml_entries.sort(key=lambda x: x['id'])
yaml_data = {'sources': yaml_entries}

yaml_file = source_dir / ".." / "sources.yaml"
with open(yaml_file, 'w') as yf:
    yaml.dump(yaml_data, yf, default_flow_style=False, sort_keys=False)

print(f"Regenerated sources.yaml with {len(yaml_entries)} entries.")

