import requests

def scrape_sleeper():
    print("   > Contacting Sleeper API...", end="\r")
    url = "https://sleeper.com/graphql"
    
    # 🚨 FIX: New Query Name is 'player_projections' (old 'pl_get_all...' is dead)
    query = """
    query list_player_projections($sport: SportType!, $filters: PlayerProjectionsFilters!) {
      player_projections(sport: $sport, filters: $filters) {
        player {
          first_name
          last_name
          team
        }
        line_score
        stat_type
        board_time
      }
    }
    """
    
    # Updated variables to match the new query structure
    variables = {
        "sport": "nba",
        "filters": {} # Empty filter = Get all active lines
    }
    
    payload = {
        "operationName": "list_player_projections",
        "variables": variables,
        "query": query
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"   > ⚠️ Sleeper Error: {response.status_code}"); return []

        data = response.json()
        
        # Check if the API sent back an error message (like the one in your debug)
        if 'errors' in data:
            print(f"   > ❌ Sleeper API Error: {data['errors'][0].get('message')}")
            return []

        # Parse the new data path: data -> player_projections
        projections = data.get('data', {}).get('player_projections', [])
        
        props = []
        for proj in projections:
            player = proj.get('player')
            if not player: continue
            
            # Sleeper lines can sometimes be None if the prop is locked
            line = proj.get('line_score')
            if line is None: continue

            props.append({
                'name': f"{player['first_name']} {player['last_name']}",
                'line': float(line),
                'stat': proj.get('stat_type'),
                'app': 'sleeper'
            })
            
        return props

    except Exception as e:
        print(f"   > ❌ Sleeper Crash: {e}")
        return []