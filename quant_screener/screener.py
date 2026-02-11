# screener.py
import config
from quant_engine import get_shin_true_probs, calculate_ev, kelly_criterion
from models import EVBet
from utils import find_best_match

def find_value_bets(games_data, scraped_data=None, bankroll=1000):
    """
    Scans data for +EV opportunities and Safe/Grinder plays.
    """
    bets_found = []
    PP_IMPLIED_PROB = 0.543  # Break-even point for PrizePicks/Underdog (54.3%)

    for game in games_data:
        # 1. Locate the Sharp Book (Pinnacle)
        sharp_book = next((b for b in game['bookmakers'] if b['key'] in config.SHARP_BOOKS), None)
        
        # If no sharp odds exist for this game, we can't price it. Skip.
        if not sharp_book: 
            continue 

        for market in sharp_book['markets']:
            is_prop = "player" in market['key']
            outcomes = market['outcomes']
            
            # Extract Sharp Odds
            sharp_odds = [o['price'] for o in outcomes]
            
            # 2. Calculate "True" Probability (Devigging)
            try:
                true_probs = get_shin_true_probs(sharp_odds)
            except Exception:
                continue # Skip if math fails

            # --- BRANCH A: STANDARD BETTING (Moneyline, Spreads, Totals) ---
            if not is_prop:
                team_names = [o['name'] for o in outcomes]
                true_prob_map = dict(zip(team_names, true_probs))

                for book in game['bookmakers']:
                    # Only check "Soft" books
                    if book['key'] not in config.SOFT_BOOKS:
                        continue

                    soft_market = next((m for m in book['markets'] if m['key'] == market['key']), None)
                    if not soft_market: 
                        continue

                    for outcome in soft_market['outcomes']:
                        team = outcome['name']
                        price = outcome['price']
                        
                        if team not in true_prob_map: 
                            continue
                        
                        true_p = true_prob_map[team]
                        ev = calculate_ev(price, true_p)

                        # --- DUAL-TRACK SCANNING LOGIC ---
                        
                        # 1. Is it a Value Bet? (High Edge)
                        is_value = (ev > config.MIN_EDGE) and (price >= config.MIN_ODDS)

                        # 2. Is it a Safe/Grinder Bet? (High Probability)
                        is_safe = False
                        if config.ENABLE_SAFE_BETS:
                            is_safe = (
                                true_p >= config.MIN_SAFE_PROB and
                                ev >= config.MIN_SAFE_EDGE and
                                price <= config.MAX_SAFE_ODDS
                            )

                        # Execution
                        if is_value or is_safe:
                            # Tag the bet type for the user
                            tag = "🛡️ SAFE" if is_safe else "💰 VALUE"
                            
                            # Adjust stake: Safe bets often allow higher sizing (Kelly), 
                            # but we stick to the config multiplier for safety.
                            stake = kelly_criterion(price, true_p, bankroll, config.KELLY_MULTIPLIER)
                            
                            bet_obj = create_bet_obj(game, f"{tag} {team}", book['key'], price, true_p, ev, stake)
                            bets_found.append(bet_obj)
            
            # --- BRANCH B: PLAYER PROPS (DFS / Sniping) ---
            elif scraped_data and is_prop:
                for i, outcome in enumerate(outcomes):
                    true_p = true_probs[i]
                    sharp_name = outcome.get('description') # e.g., "LeBron James"
                    sharp_line = outcome.get('point')       # e.g., 24.5
                    side = outcome['name']                  # 'Over' or 'Under'

                    if not sharp_name or not sharp_line:
                        continue

                    # Check across all enabled scrapers (PrizePicks, Underdog, etc.)
                    for app_name, players in scraped_data.items():
                        if not players: continue
                        
                        # Fuzzy Match: Find this player in the DFS app
                        app_player_names = [p.get('name') for p in players]
                        matched_name = find_best_match(sharp_name, app_player_names)

                        if matched_name:
                            # Get the line from the app (e.g., PrizePicks line)
                            app_player = next(p for p in players if p['name'] == matched_name)
                            app_line = app_player.get('line')
                            if not app_line: continue

                            # 🚨 CHECK FOR DISCREPANCIES 🚨
                            # Example: Sharp says 24.5 (-140), PrizePicks says 22.5. 
                            # Taking Over 22.5 is massive value.
                            is_discrepancy = False
                            if side == 'Over' and app_line < sharp_line: is_discrepancy = True
                            if side == 'Under' and app_line > sharp_line: is_discrepancy = True

                            # DFS "Safe" logic: If the Sharp Probability is super high (>58%), it's a lock.
                            is_high_prob = (true_p > 0.58)

                            if is_high_prob or is_discrepancy:
                                ev = true_p - PP_IMPLIED_PROB
                                
                                # Tagging
                                if is_discrepancy:
                                    bonus_text = f"🔥 LINE GAP ({app_line} vs {sharp_line})"
                                else:
                                    bonus_text = "💎 HIGH PROB"
                                
                                bet = EVBet(
                                    game=f"{game['home_team']} vs {game['away_team']}",
                                    team=f"{bonus_text} {matched_name} {side} {app_line}",
                                    bookmaker=app_name.upper(),
                                    odds=1.84, # Standard payout for 5-pick flex (-119 implied)
                                    true_prob=true_p,
                                    ev=ev,
                                    kel_stake=0 # DFS usually fixed unit size
                                )
                                bets_found.append(bet)

    return bets_found

def create_bet_obj(game, team, book, price, true_p, ev, stake):
    return EVBet(
        game=f"{game['home_team']} vs {game['away_team']}",
        team=team, 
        bookmaker=book, 
        odds=price,
        true_prob=true_p, 
        ev=ev, 
        kel_stake=stake
    )