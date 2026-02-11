import requests
import uuid

def scrape_underdog():
    print("   > Contacting Underdog API...", end="\r")
    url = "https://api.underdogfantasy.com/beta/v3/over_under_lines"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "client-device-id": str(uuid.uuid4())
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200: return []
        
        data = res.json()
        
        # FIX: The debug showed data is in 'appearances', not 'over_under_lines'
        # We combine both lists just to be safe.
        items = data.get('appearances', []) + data.get('over_under_lines', [])
        
        props = []
        for item in items:
            # Sometimes the prop info is nested in 'over_under', sometimes it's direct
            # We try to grab the title and value from a few possible spots
            
            # Case A: Nested in 'over_under' (Standard)
            ou = item.get('over_under', {})
            title = ou.get('title') or item.get('title')
            val = ou.get('stat_value') or ou.get('line_score') or item.get('stat_value')
            stat = ou.get('stat') or item.get('stat') # Sometimes explicit

            # Case B: If 'title' is missing, maybe construct it? 
            # (Skipping complex reconstruction to keep it stable)
            
            if not title or val is None: continue

            try:
                # "LeBron James Points" -> Name: LeBron James, Stat: Points
                parts = title.rsplit(' ', 1)
                if len(parts) == 2:
                    props.append({
                        'name': parts[0],
                        'line': float(val),
                        'stat': parts[1],
                        'app': 'underdog'
                    })
            except: continue
            
        return props

    except Exception as e:
        print(f"   > ❌ Underdog Crash: {e}"); return []