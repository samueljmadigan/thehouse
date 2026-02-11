# quant_engine.py
import math
from scipy.optimize import minimize

def implied_prob(decimal_odds):
    """Simple inverse of odds."""
    return 1 / decimal_odds

def shin_error_func(z, implied_probs):
    """
    Optimization function for Shin's method.
    z = proportion of insider trading volume.
    """
    z = z[0]
    sum_probs = 0
    for ip in implied_probs:
        # Avoid domain errors in sqrt
        try:
            term = math.sqrt(z**2 + 4 * (1 - z) * ip**2 / sum(implied_probs))
            sum_probs += (term - z) / (2 * (1 - z))
        except ValueError:
            return 100 
    return (sum_probs - 1.0)**2

def get_shin_true_probs(odds_list: list[float]) -> list[float]:
    """
    Calculates the TRUE, No-Vig probability using Shin's method.
    """
    implied_probs = [implied_prob(o) for o in odds_list]
    
    # Solve for z (insider trading factor)
    res = minimize(
        shin_error_func, 
        x0=[0.01], 
        args=(implied_probs,), 
        bounds=[(0, 0.99)], 
        method='L-BFGS-B'
    )
    
    z_opt = res.x[0]
    pi_sum = sum(implied_probs)
    true_probs = []
    
    for ip in implied_probs:
        term = math.sqrt(z_opt**2 + 4 * (1 - z_opt) * ip**2 / pi_sum)
        tp = (term - z_opt) / (2 * (1 - z_opt))
        true_probs.append(tp)
        
    return true_probs

def calculate_ev(offered_odds, true_prob):
    """EV = (Prob_Win * Profit) - (Prob_Loss * Stake)"""
    return (true_prob * (offered_odds - 1)) - ((1 - true_prob) * 1)

def kelly_criterion(odds, true_prob, bankroll, multiplier):
    """Standard Kelly Formula with fractional sizing."""
    b = odds - 1
    p = true_prob
    q = 1 - p
    f = (b * p - q) / b
    return max(0, f * bankroll * multiplier)