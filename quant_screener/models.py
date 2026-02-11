# models.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MarketOutcome:
    name: str
    price: float  # Decimal Odds
    point: Optional[float] = None # For spreads/totals

@dataclass
class GameOdds:
    bookmaker: str
    outcomes: List[MarketOutcome]
    
@dataclass
class EVBet:
    game: str
    team: str
    bookmaker: str
    odds: float
    true_prob: float
    ev: float
    kel_stake: float