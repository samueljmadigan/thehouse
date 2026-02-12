# config.py

# --- API KEYS ---
# 🚨 SECURITY WARNING: You posted this key in chat. ROTATE IT NOW at https://the-odds-api.com/
# After rotating, paste the NEW key inside the quotes below.
API_KEY = "d926d60e4602dd8367e8ab46d6b07b66" 

# DISCORD_WEBHOOK = "your_webhook_url_here" # (Uncomment if you use this)

# --- STRATEGY SETTINGS ---
# 1. Standard Value Bets (High Edge)
MIN_EDGE = 0.015          # Minimum 2.5% EV to trigger a bet
KELLY_MULTIPLIER = 0.2   # Fractional Kelly (conservative)
MIN_ODDS = 1.2           # Minimum Decimal Odds (-200 American)
MAX_ODDS = 4.2          # Maximum Decimal Odds (+300 American)

# 2. Safe / Grinder Bets (High Probability)
# These settings look for lower returns but much higher win rates (65%+)
ENABLE_SAFE_BETS = True
MIN_SAFE_PROB = 0.65      # Only bet if Win Probability is > 65%
MAX_SAFE_ODDS = 1.45      # Max Decimal Odds (-220) for "Safe" tier
MIN_SAFE_EDGE = 0.015     # Lower threshold (1.5%) is acceptable for safe bets

# --- SCHEDULE SETTINGS (The 3-Minute Strategy) ---
SCAN_INTERVAL = 180       # 3 minutes in seconds
START_HOUR = 9            # 9 AM
END_HOUR = 22             # 10 PM

# --- BOOKMAKER SETTINGS ---
SHARP_BOOKS = ['pinnacle']                                   # The "Truth" (Market Makers)
SOFT_BOOKS = ['draftkings', 'fanduel', 'betmgm', 'caesars']  # The Targets

# --- SCRAPER / APP SETTINGS ---
ENABLE_PRIZEPICKS = True
ENABLE_UNDERDOG = True
ENABLE_SLEEPER = False

# App-specific IDs
SPORT_IDS = {
    'prizepicks': {'nba': 7, 'nhl': 12, 'ncaab': 15},
    'sleeper': {'nba': 'nba', 'nhl': 'nhl', 'ncaab': 'ncaab'},
    'underdog': {'nba': 'nba', 'nhl': 'nhl', 'ncaab': 'ncaab'}
}

# --- TECHNICAL SETTINGS ---
# Browser disguise to avoid getting blocked
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

SCRAPE_DELAY = 600
