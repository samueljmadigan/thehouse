import requests
import config

def fetch_odds(sport='basketball_nba', markets='h2h'):
    """
    Fetches REAL odds from The-Odds-API.
    Uses Event-Specific endpoint for Props and Bulk for Game Lines.
    """
    # 1. SETUP - Check if we are doing props or game lines
    is_prop = "player" in markets

    # If it's a standard game line (h2h, spreads, totals), use the Bulk endpoint
    if not is_prop:
        url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds'
        params = {
            'apiKey': config.API_KEY,
            'regions': 'us', 
            'markets': markets,
            'oddsFormat': 'decimal'
        }
        try:
            res = requests.get(url, params=params)
            return res.json() if res.status_code == 200 else []
        except: return []

    # 2. PROPS MODE: Fetch Event IDs first
    events_url = f"https://api.the-odds-api.com/v4/sports/{sport}/events"
    try:
        events_res = requests.get(events_url, params={'apiKey': config.API_KEY})
        if events_res.status_code != 200: return []
        events = events_res.json()
    except: return []

    all_data = []
    # 3. Fetch specific props for the first 8 games (to save API credits)
    for event in events[:8]:
        event_id = event['id']
        prop_url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds"
        prop_params = {
            'apiKey': config.API_KEY,
            'regions': 'us',
            'markets': markets,
            'oddsFormat': 'decimal'
        }
        try:
            res = requests.get(prop_url, params=prop_params)
            if res.status_code == 200:
                all_data.append(res.json())
        except: continue

    return all_data