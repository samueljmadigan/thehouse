# quant_screener/test_scrapers.py
import sys
import os

# Ensure the script can see the parent folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.prizepicks import scrape_prizepicks
from scrapers.underdog import scrape_underdog
from scrapers.sleeper import scrape_sleeper
import config

print("--- DIAGNOSTIC MODE ---")

# 1. Test PrizePicks
if config.ENABLE_PRIZEPICKS:
    print("\n1. Testing PrizePicks...")
    pp_data = scrape_prizepicks()
    if pp_data:
        print(f"✅ Success! Found {len(pp_data)} props.")
        print(f"Sample: {pp_data[0]}")
    else:
        print("❌ Failed: Found 0 props.")

# 2. Test Underdog
if config.ENABLE_UNDERDOG:
    print("\n2. Testing Underdog...")
    ud_data = scrape_underdog()
    if ud_data:
        print(f"✅ Success! Found {len(ud_data)} props.")
    else:
        print("❌ Failed: Found 0 props.")

# 3. Test Sleeper
if config.ENABLE_SLEEPER:
    print("\n3. Testing Sleeper...")
    sl_data = scrape_sleeper()
    if sl_data:
        print(f"✅ Success! Found {len(sl_data)} props.")
    else:
        print("❌ Failed: Found 0 props.")