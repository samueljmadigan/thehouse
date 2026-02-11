import requests
import config
import json

def fetch_odds(sport='basketball_nba', markets='h2h'):
    """
    Fetches REAL odds from The-Odds-API.
    Supports 'h2h' (Moneyline) and player props (e.g., 'player_points').
    """
    # 1. SETUP
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds'
    params = {
        'apiKey': config.API_KEY,
        'regions': 'us,eu', 
        'markets': markets, # Dynamic: defaults to h2h, but can accept props
        'oddsFormat': 'decimal'
    }

    # SECURITY NOTE: Debug print removed. 
    # Your API Key is now hidden from the terminal.

    try:
        # 2. REQUEST
        response = requests.get(url, params=params)
        
        # 3. CHECK FOR ERRORS
        if response.status_code != 200:
            print(f"\n❌ API ERROR: {response.text}")
            print("👉 TIP: Check your config.py if you see a 401 error.\n")
            return []
            
        return response.json()
        
    except Exception as e:
        print(f"Network error: {e}")
        return []