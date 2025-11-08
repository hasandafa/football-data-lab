"""
Transfer system module
Handles player transfers between clubs
Note: This is a simplified version for initial data generation.
Full transfer logic will be implemented in match simulation.
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from src.config import TRANSFER_CONFIG, RANDOM_SEED
from src.utils import generate_id

random.seed(RANDOM_SEED)


def generate_transfer_record(
    player_id: str,
    player_name: str,
    from_club: str,
    to_club: str,
    season: str,
    transfer_window: str,
    transfer_type: str = "permanent",
    transfer_fee: int = 0,
    age: int = 25,
    ability: float = 70.0
) -> dict:
    """
    Generate a transfer record
    
    Args:
        player_id: Player identifier
        player_name: Player's full name
        from_club: Club selling/loaning player
        to_club: Club buying/loaning player
        season: Season of transfer
        transfer_window: "summer" or "winter"
        transfer_type: "permanent", "loan", or "free"
        transfer_fee: Transfer fee amount
        age: Player age at transfer
        ability: Player ability rating at transfer
        
    Returns:
        Dictionary with transfer information
    """
    # Generate transfer date
    season_year = int(season.split("/")[0])
    
    if transfer_window == "summer":
        month = random.randint(6, 8)  # June to August
    else:
        month = 1  # January
    
    day = random.randint(1, 28)
    transfer_date = f"{season_year}-{month:02d}-{day:02d}"
    
    # Contract length (1-5 years)
    contract_length = random.randint(1, 5) if transfer_type != "loan" else 1
    
    # Weekly wage estimate (roughly 1% of transfer fee annually / 52 weeks)
    if transfer_fee > 0:
        weekly_wage = int((transfer_fee * 0.01) / 52)
    else:
        weekly_wage = int(ability * random.uniform(500, 1500))
    
    # Transfer reason
    reasons = [
        "Career progression",
        "Higher wages",
        "First team opportunity",
        "Playing time",
        "Relegation clause",
        "Contract expiry",
        "Club financial needs",
        "Manager request"
    ]
    
    return {
        "transfer_id": generate_id("TRF", random.randint(1, 999999)),
        "season": season,
        "transfer_window": transfer_window,
        "date": transfer_date,
        "player_id": player_id,
        "player_name": player_name,
        "from_club": from_club,
        "to_club": to_club,
        "transfer_type": transfer_type,
        "transfer_fee": transfer_fee,
        "contract_length_years": contract_length,
        "weekly_wage": weekly_wage,
        "player_age": age,
        "player_ability": ability,
        "reason": random.choice(reasons)
    }


def create_initial_transfer_history(
    players: pd.DataFrame,
    clubs: pd.DataFrame,
    seasons: list
) -> pd.DataFrame:
    """
    Create initial transfer history for past seasons (optional/placeholder)
    
    Args:
        players: DataFrame of all players
        clubs: DataFrame of all clubs
        seasons: List of past seasons
        
    Returns:
        DataFrame with transfer history
    """
    # For initial generation, we'll create minimal transfer history
    # Full transfer simulation will happen during season simulation
    
    transfers = []
    
    # Placeholder: Generate a few random historical transfers
    num_historical_transfers = len(players) // 10  # 10% of players changed clubs
    
    sample_players = players.sample(n=min(num_historical_transfers, len(players)))
    club_names = clubs["full_name"].tolist()
    
    for _, player in sample_players.iterrows():
        # Random past season
        past_season = random.choice(seasons[:-1]) if len(seasons) > 1 else seasons[0]
        transfer_window = random.choice(["summer", "winter"])
        
        # Random clubs (different from current)
        available_clubs = [c for c in club_names if c != player.get("club_id", "")]
        if available_clubs:
            from_club = random.choice(available_clubs)
            to_club = player.get("club_id", random.choice(club_names))
            
            # Random transfer fee based on ability
            if random.random() < TRANSFER_CONFIG["free_transfer_ratio"]:
                transfer_type = "free"
                fee = 0
            elif random.random() < TRANSFER_CONFIG["loan_ratio"]:
                transfer_type = "loan"
                fee = 0
            else:
                transfer_type = "permanent"
                fee = int(player.get("market_value", 1000000) * random.uniform(0.7, 1.3))
            
            transfer = generate_transfer_record(
                player_id=player["player_id"],
                player_name=player["full_name"],
                from_club=from_club,
                to_club=to_club,
                season=past_season,
                transfer_window=transfer_window,
                transfer_type=transfer_type,
                transfer_fee=fee,
                age=player["age"],
                ability=player["overall_rating"]
            )
            
            transfers.append(transfer)
    
    return pd.DataFrame(transfers) if transfers else pd.DataFrame()


if __name__ == "__main__":
    print("Transfer module loaded. Full transfer simulation will occur during season generation.")