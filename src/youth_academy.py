"""
Youth Academy module
Handles youth player generation and promotion to first team
"""

import pandas as pd
import random
from typing import Tuple
from src.config import YOUTH_ACADEMY_CONFIG, RANDOM_SEED
from src.players import generate_player

random.seed(RANDOM_SEED)


def generate_youth_academy_players(
    club_id: str,
    num_players: int = None,
    season: str = "2024/25"
) -> pd.DataFrame:
    """
    Generate youth academy players for a club
    
    Args:
        club_id: Club identifier
        num_players: Number of youth players to generate
        season: Current season
        
    Returns:
        DataFrame with youth academy players
    """
    if num_players is None:
        num_players = YOUTH_ACADEMY_CONFIG["players_per_season"]
    
    youth_players = []
    
    # Generate players aged 16-17
    for i in range(num_players):
        age = random.randint(*YOUTH_ACADEMY_CONFIG["age_range"])
        position_group = random.choice(["GK", "DEF", "MID", "FWD"])
        
        # Youth players have lower current ability but varying potential
        player_data = generate_player(
            player_id=10000 + i,  # High numbers for youth
            club_id=club_id,
            position_group=position_group,
            age=age,
            season=season
        )
        
        # Adjust for youth - lower current ability
        player_data["overall_rating"] = max(40, player_data["overall_rating"] - 15)
        
        # Potential varies - some are elite prospects
        potential_category = random.choices(
            ["average", "good", "high", "elite"],
            weights=[0.40, 0.40, 0.15, 0.05],
            k=1
        )[0]
        
        potential_ranges = {
            "average": (50, 59),
            "good": (60, 69),
            "high": (70, 79),
            "elite": (80, 90)
        }
        
        player_data["potential"] = random.randint(*potential_ranges[potential_category])
        player_data["is_youth"] = True
        player_data["youth_entry_year"] = int(season.split("/")[0])
        
        youth_players.append(player_data)
    
    return pd.DataFrame(youth_players)


def identify_promotion_candidates(
    youth_players: pd.DataFrame,
    season: str = "2024/25"
) -> pd.DataFrame:
    """
    Identify youth players ready for first team promotion
    
    Args:
        youth_players: DataFrame of youth academy players
        season: Current season
        
    Returns:
        DataFrame of players eligible for promotion
    """
    if youth_players.empty:
        return pd.DataFrame()
    
    # Filter for promotion candidates
    candidates = youth_players[
        (youth_players["age"] >= YOUTH_ACADEMY_CONFIG["promotion_age"]) &
        (youth_players["overall_rating"] >= YOUTH_ACADEMY_CONFIG["min_ability_for_promotion"]) &
        (youth_players["potential"] >= YOUTH_ACADEMY_CONFIG["min_potential_for_promotion"])
    ].copy()
    
    return candidates


def promote_youth_players(
    youth_players: pd.DataFrame,
    first_team: pd.DataFrame,
    num_promotions: int = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Promote youth players to first team
    
    Args:
        youth_players: DataFrame of youth academy players
        first_team: DataFrame of first team players
        num_promotions: Number of players to promote (if None, promotes all eligible)
        
    Returns:
        Tuple of (updated_first_team, remaining_youth_players)
    """
    candidates = identify_promotion_candidates(youth_players)
    
    if candidates.empty:
        return first_team, youth_players
    
    # If num_promotions specified, select top candidates by potential
    if num_promotions is not None:
        candidates = candidates.nlargest(num_promotions, "potential")
    
    # Remove is_youth flag for promoted players
    candidates["is_youth"] = False
    
    # Add to first team
    updated_first_team = pd.concat([first_team, candidates], ignore_index=True)
    
    # Remove from youth academy
    remaining_youth = youth_players[
        ~youth_players["player_id"].isin(candidates["player_id"])
    ]
    
    return updated_first_team, remaining_youth


if __name__ == "__main__":
    # Test youth academy
    print("Generating youth academy players...")
    youth = generate_youth_academy_players("CLB_00001", num_players=6)
    print(f"Generated {len(youth)} youth players")
    print(youth[["full_name", "age", "position_group", "overall_rating", "potential"]])
    
    print("\n\nIdentifying promotion candidates...")
    # Simulate some development
    youth.loc[youth.index[0:2], "age"] = 18
    youth.loc[youth.index[0:2], "overall_rating"] = 60
    youth.loc[youth.index[0:2], "potential"] = 75
    
    candidates = identify_promotion_candidates(youth)
    print(f"Found {len(candidates)} promotion candidates")
    print(candidates[["full_name", "age", "overall_rating", "potential"]])