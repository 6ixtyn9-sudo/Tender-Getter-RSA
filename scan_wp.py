import json, ssl, yaml
from pathlib import Path
from urllib.request import urlopen, Request
import concurrent.futures

YAML_PATH = Path("src/tender_getter/sources.yaml")
SRC_DIR = Path("src/tender_getter/sources")

def get_ssl_ctx():
    try:
        return ssl._create_unverified_context()
    except:
        return None

def check_wp(source):
    url = source.get('url', '').rstrip('/')
    if not url.startswith('http'):
        return None
        
    # Check if already wp_api
    src_file = next(SRC_DIR.rglob(f"{source['id']}.py"), None)
    if src_file and "wp_fetch_tenders" in src_file.read_text():
        return None
        
    api_url = f"{url}/wp-json/wp/v2/types"
    ctx = get_ssl_ctx()
    req = Request(api_url, headers={"User-Agent": "Tender-Getter-RSA/2.0"})
    
    try:
        with urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read())
            
        candidates = []
        for type_slug, type_info in data.items():
            name = type_info.get('name', '').lower()
            slug = type_slug.lower()
            if any(k in name or k in slug for k in ['tender', 'procure', 'scm', 'bid', 'supply']):
                candidates.append(type_slug)
                
        if candidates:
            return {'id': source['id'], 'url': url, 'types': candidates}
    except Exception:
        pass
        
    return None

def main():
    with YAML_PATH.open() as f:
        data = yaml.safe_load(f)
        sources = data['sources']
        
    print(f"Scanning {len(sources)} sources for WP API...")
    
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check_wp, sources)
        for r in results:
            if r:
                found.append(r)
                print(f"Found WP API for {r['id']}: {r['types']}")
                
    with open("wp_candidates.json", "w") as f:
        json.dump(found, f, indent=2)

if __name__ == "__main__":
    main()
