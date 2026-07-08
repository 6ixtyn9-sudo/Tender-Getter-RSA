import os
import glob
from pathlib import Path

sources_dir = Path('src/tender_getter/sources')

# 1. Rename files and update source_id in files
for filepath in sources_dir.rglob("*.py"):
    if filepath.name in ("__init__.py", "common.py", "generic.py"):
        continue

    content = filepath.read_text()
    
    # Remove _tenders from source_id
    if 'source_id: str = "' in content:
        import re
        content = re.sub(r'(source_id:\s*str\s*=\s*"[^"]+)_tenders(")', r'\1\2', content)
        filepath.write_text(content)
        
    # Rename file if it ends with _tenders.py
    if filepath.name.endswith('_tenders.py'):
        new_name = filepath.name.replace('_tenders.py', '.py')
        new_filepath = filepath.parent / new_name
        filepath.rename(new_filepath)

# 2. Re-run YAML merge
import subprocess
print("Regenerating YAML...")
subprocess.run(["python3", "scripts/merge_yaml.py"], check=True)

# 3. Clean up empty directories
def remove_empty_dirs(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")
            except OSError:
                pass

remove_empty_dirs(str(sources_dir))

print("Done removing 'tenders' from sources.")
