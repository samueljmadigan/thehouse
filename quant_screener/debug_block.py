import requests
import uuid

def test_connection():
    print("--- DIAGNOSTIC NETWORK TEST ---")
    
    # 1. Test Underdog
    url = "https://api.underdogfantasy.com/beta/v3/over_under_lines"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "client-device-id": str(uuid.uuid4())
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"\nUNDERDOG STATUS: {r.status_code}")
        print(f"Response Data Sample: {str(r.json())[:100]}...") 
        # If this says 'over_under_lines': [], you are Soft Blocked.
    except Exception as e:
        print(f"Underdog Error: {e}")

    # 2. Test Sleeper
    url = "https://sleeper.com/graphql"
    query = """query pl_get_all_player_projections($sport: String!, $filters: ProjectionFilters) { pl_get_all_player_projections(sport: $sport, filters: $filters) { player { first_name } } }"""
    try:
        r = requests.post(url, json={"operationName":"pl_get_all_player_projections","variables":{"sport":"nba","filters":{}},"query":query}, timeout=5)
        print(f"\nSLEEPER STATUS: {r.status_code}")
        print(f"Response Data Sample: {str(r.json())[:100]}...")
        # If this data is empty or null, you are Soft Blocked.
    except Exception as e:
        print(f"Sleeper Error: {e}")

if __name__ == "__main__":
    test_connection()