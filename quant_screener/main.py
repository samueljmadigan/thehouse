import os
import sys
from datetime import datetime
import config
from odds_fetcher import fetch_odds
from screener import find_value_bets
from alerts import send_discord_alert

# Import Scrapers
from scrapers.prizepicks import scrape_prizepicks
from scrapers.underdog import scrape_underdog
# Sleeper is disabled for now

# ✅ PAID PLAN ENABLED: We can now scan these props!
PROP_MARKETS = [
    'player_points', 
    'player_rebounds', 
    'player_assists',
    'player_threes',
    'h2h' # Also check game winners
]

def get_market_for_current_time():
    """Rotates through markets based on the minute of the hour."""
    minute = datetime.now().minute
    # 0-12: Points, 12-24: Rebounds, 24-36: Assists, 36-48: Threes, 48-60: H2H
    index = (minute // 12) % len(PROP_MARKETS)
    return PROP_MARKETS[index]

def run_iteration():
    print("--- 🚀 QUANT SNIPER: PAID TIER MODE ---")
    
    # 1. Select Market
    current_market = get_market_for_current_time()
    print(f"🎯 Target Market: {current_market}")

    scraped_data = {}

    # 2. Scrape DFS Apps (Only needed for player props)
    if "player" in current_market:
        print("   > Scraping DFS Apps...")
        try:
            if config.ENABLE_PRIZEPICKS: scraped_data['prizepicks'] = scrape_prizepicks()
            if config.ENABLE_UNDERDOG:   scraped_data['underdog'] = scrape_underdog()
        except Exception as e:
            print(f"   ⚠️ Scraping Error: {e}")

    # 3. Scan Sports
    # We scan NBA, NHL, and NCAAB
    sports = ['nba', 'nhl', 'ncaab'] 
    
    for sport in sports:
        print(f"\nScanning {sport.upper()}...")
        
        # Convert to API keys
        api_sport = f"icehockey_{sport}" if sport == 'nhl' else f"basketball_{sport}"
        
        try:
            # A. Fetch Odds (Using your Paid Key)
            # Note: We fetch 'us' bookmakers. If you are in UK/EU, change region='eu'
            sharp_data = fetch_odds(api_sport, markets=current_market)
            
            # B. Check for valid data
            if not sharp_data:
                print(f"   ⚠️ API returned no odds for {sport} (Check your plan/quota).")
                continue
                
            # C. Find Edges
            opportunities = find_value_bets(sharp_data, scraped_data, bankroll=5000)
            
            # D. Alert
            if opportunities:
                print(f"   🔥 Found {len(opportunities)} edges!")
                for bet in opportunities:
                    send_discord_alert(bet)
            else:
                print("   💤 No edges found.")
                
        except Exception as e:
            print(f"   ❌ Failed to scan {sport}: {e}")

if __name__ == "__main__":
    # Run immediately (GitHub controls the schedule)
    run_iteration()