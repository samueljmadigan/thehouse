import requests
import json
import time

def scrape_prizepicks():
    """
    Fetches active props from the PrizePicks API.
    Returns a list of dicts: {'name': 'LeBron James', 'line': 24.5, 'type': 'Points'}
    """
    print("   > Contacting PrizePicks API...", end="\r")
    
    # PrizePicks Public API Endpoint
    url = "https://partner-api.prizepicks.com/projections"
    
    # Headers to look like a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    params = {
        "per_page": 1000,
        "single_stat": "true" # We only want single stats (e.g., Points), not combos
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"   > ❌ PrizePicks Error: {response.status_code}")
            return []

        data = response.json()
        included = data.get('included', []) # This holds the player info
        projections = data.get('data', [])  # This holds the lines
        
        # 1. Map Player IDs to Names
        player_map = {}
        for item in included:
            if item['type'] == 'new_player':
                player_map[item['id']] = item['attributes']['name']

        # 2. Parse the Projections (Lines)
        props = []
        for proj in projections:
            attrs = proj['attributes']
            player_id = proj['relationships']['new_player']['data']['id']
            
            # Skip if player not found or line is missing
            if player_id not in player_map: continue
            
            # Get key data
            name = player_map[player_id]
            stat_type = attrs.get('stat_type') # e.g., 'Points'
            line_score = attrs.get('line_score') # e.g., 24.5
            
            if line_score is None: continue

            props.append({
                'name': name,
                'line': float(line_score),
                'stat': stat_type,
                'app': 'prizepicks'
            })
            
        return props

    except Exception as e:
        print(f"   > ❌ PrizePicks Crash: {e}")
        return []