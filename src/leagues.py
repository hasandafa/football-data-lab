"""
League and competition structure generation
"""

import pandas as pd
from typing import Dict
from src.config import LEAGUE_CONFIG, SEASONS


def generate_league() -> Dict:
    """
    Generate league information
    
    Returns:
        Dictionary containing league information
    """
    league_data = {
        "league_id": "LG_001",
        "name": LEAGUE_CONFIG["name"],
        "short_name": LEAGUE_CONFIG["short_name"],
        "country": LEAGUE_CONFIG["country"],
        "num_teams": LEAGUE_CONFIG["num_teams"],
        "promotion_spots": LEAGUE_CONFIG["promotion_spots"],
        "relegation_spots": LEAGUE_CONFIG["relegation_spots"],
        "european_spots": LEAGUE_CONFIG["european_spots"],
        "season_format": "double_round_robin",  # Home and away
        "points_for_win": 3,
        "points_for_draw": 1,
        "points_for_loss": 0,
    }
    
    return league_data


def generate_season_info() -> pd.DataFrame:
    """
    Generate information for all seasons
    
    Returns:
        DataFrame with season information
    """
    season_data = []
    
    for i, season in enumerate(SEASONS):
        start_year = int(season.split("/")[0])
        end_year = start_year + 1
        
        season_info = {
            "season_id": f"S{i+1:02d}",
            "season": season,
            "start_year": start_year,
            "end_year": end_year,
            "start_date": f"{start_year}-08-01",  # Season starts in August
            "end_date": f"{end_year}-05-31",  # Season ends in May
            "num_matchdays": LEAGUE_CONFIG["matches_per_season"],
            "is_current": season == SEASONS[-1],
        }
        season_data.append(season_info)
    
    return pd.DataFrame(season_data)


def initialize_league_table(clubs: pd.DataFrame, season: str) -> pd.DataFrame:
    """
    Initialize an empty league table for a season
    
    Args:
        clubs: DataFrame of clubs
        season: Season identifier
        
    Returns:
        DataFrame with initialized league table
    """
    table_data = []
    
    for _, club in clubs.iterrows():
        table_entry = {
            "season": season,
            "club_id": club["club_id"],
            "club_name": club["full_name"],
            "position": 0,  # Will be calculated after matches
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
            "form": "",  # Last 5 results (W/D/L)
            "home_wins": 0,
            "home_draws": 0,
            "home_losses": 0,
            "away_wins": 0,
            "away_draws": 0,
            "away_losses": 0,
        }
        table_data.append(table_entry)
    
    return pd.DataFrame(table_data)


if __name__ == "__main__":
    # Test league generation
    league = generate_league()
    print("League Information:")
    print(league)
    
    print("\nSeason Information:")
    seasons = generate_season_info()
    print(seasons)