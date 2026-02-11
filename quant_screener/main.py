import os
import sys
from datetime import datetime
import config
from odds_fetcher import fetch_odds
from screener import find_value_bets
from alerts import send_discord_alert

# Import your scrapers
from scrapers.prizepicks import scrape_prizepicks
from scrapers.underdog import scrape_underdog
from scrapers.sleeper import scrape_sleeper

# --- CONFIGURATION ---
SPORTS_TO_SCAN = ['nba', 'nhl', 'ncaab'] 

# Market Rotation Strategy
PROP_MARKETS = ['player_points', 'player_rebounds', 'player_assists', 'h2h']

def get_market_for_current_time():
    """Selects a market based on the current minute to mimic rotation."""
    minute = datetime.now().minute
    # 0-15: Points, 15-30: Rebounds, 30-45: Assists, 45-60: H2H
    index = (minute // 15) % len(PROP_MARKETS)
    return PROP_MARKETS[index]

def run_iteration():
    print("--- 🚀 QUANT SNIPER: GITHUB ACTIONS MODE ---")
    
    # 1. Select Market (Stateless Rotation)
    current_market = get_market_for_current_time()
    print(f"🎯 Target Market: {current_market}")

    scraped_data = {}

    # 2. Scrape All Apps (If checking player props)
    if "player" in current_market:
        print("   > Scraping DFS Apps...")
        try:
            if config.ENABLE_PRIZEPICKS: scraped_data['prizepicks'] = scrape_prizepicks()
            if config.ENABLE_UNDERDOG:   scraped_data['underdog'] = scrape_underdog()
            if config.ENABLE_SLEEPER:    scraped_data['sleeper'] = scrape_sleeper()
        except Exception as e:
            print(f"   ⚠️ Scraping Error: {e}")

    # 3. Scan Sports
    for sport in SPORTS_TO_SCAN:
        print(f"\nScanning {sport.upper()}...")
        
        # Convert to API keys (e.g. 'nba' -> 'basketball_nba')
        api_sport = f"icehockey_{sport}" if sport == 'nhl' else f"basketball_{sport}"
        
        try:
            # A. Fetch Odds
            sharp_data = fetch_odds(api_sport, markets=current_market)
            
            # B. Find Edges
            opportunities = find_value_bets(sharp_data, scraped_data, bankroll=5000)
            
            # C. Alert
            if opportunities:
                print(f"   🔥 Found {len(opportunities)} edges!")
                for bet in opportunities:
                    send_discord_alert(bet)
            else:
                print("   💤 No edges found.")
                
        except Exception as e:
            print(f"   ❌ Failed to scan {sport}: {e}")

if __name__ == "__main__":
    # Check strict hours (UTC Time) before running
    # GitHub uses UTC. 9AM CST = 15:00 UTC. 10PM CST = 04:00 UTC.
    current_hour = datetime.utcnow().hour
    
    # Simple check: Run only between 14:00 (8AM CST) and 05:00 (11PM CST)
    # Adjust these numbers if you want different hours
    if 14 <= current_hour or current_hour <= 5:
        run_iteration()
    else:
        print(f"🌙 Off-hours (Current UTC: {current_hour}:00). Skipping scan.")