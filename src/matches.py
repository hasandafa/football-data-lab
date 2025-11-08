"""
Match simulation module
Handles match generation and simulation
Note: This is a simplified version for initial data generation.
Full match simulation will be implemented separately.
"""

import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Tuple
from src.config import MATCH_CONFIG, RANDOM_SEED
from src.utils import generate_id, simulate_match_score

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def generate_season_fixtures(
    clubs: pd.DataFrame,
    season: str
) -> pd.DataFrame:
    """
    Generate all fixtures for a season (double round-robin)
    
    Args:
        clubs: DataFrame of clubs
        season: Season identifier
        
    Returns:
        DataFrame with all fixtures
    """
    club_ids = clubs["club_id"].tolist()
    club_names = clubs["full_name"].tolist()
    num_clubs = len(clubs)
    
    fixtures = []
    match_id_counter = 1
    
    # Season start date
    season_year = int(season.split("/")[0])
    start_date = datetime(season_year, 8, 15)  # Mid-August
    
    matchday = 1
    current_date = start_date
    
    # Generate home and away fixtures
    for round_num in range(2):  # Home and away
        for i in range(num_clubs):
            for j in range(i + 1, num_clubs):
                if round_num == 0:
                    home_idx, away_idx = i, j
                else:
                    home_idx, away_idx = j, i  # Reverse for away fixtures
                
                fixture = {
                    "match_id": generate_id("MTH", match_id_counter),
                    "season": season,
                    "matchday": matchday,
                    "date": current_date.strftime("%Y-%m-%d"),
                    "home_club_id": club_ids[home_idx],
                    "home_club_name": club_names[home_idx],
                    "away_club_id": club_ids[away_idx],
                    "away_club_name": club_names[away_idx],
                    "home_goals": None,  # To be filled during simulation
                    "away_goals": None,
                    "status": "scheduled"
                }
                
                fixtures.append(fixture)
                match_id_counter += 1
        
        # Space out fixtures (roughly 1 week between matches)
        if matchday % (num_clubs // 2) == 0:
            current_date += timedelta(days=7)
        
        matchday += 1
    
    return pd.DataFrame(fixtures)


def simulate_season_matches(
    fixtures: pd.DataFrame,
    clubs: pd.DataFrame,
    players: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Simulate all matches for a season
    
    Args:
        fixtures: DataFrame of fixtures
        clubs: DataFrame of clubs
        players: DataFrame of all players
        
    Returns:
        Tuple of (simulated_fixtures, updated_league_table)
    """
    from src.leagues import initialize_league_table
    
    # Initialize league table
    season = fixtures["season"].iloc[0]
    league_table = initialize_league_table(clubs, season)
    
    # Calculate average team strengths
    team_strengths = {}
    for _, club in clubs.iterrows():
        club_players = players[players["club_id"] == club["club_id"]]
        if not club_players.empty:
            team_strengths[club["club_id"]] = club_players["overall_rating"].mean()
        else:
            team_strengths[club["club_id"]] = 65.0  # Default
    
    # Simulate each match
    for idx, match in fixtures.iterrows():
        home_strength = team_strengths[match["home_club_id"]]
        away_strength = team_strengths[match["away_club_id"]]
        
        # Simulate score
        home_goals, away_goals = simulate_match_score(
            home_strength,
            away_strength,
            MATCH_CONFIG["home_advantage"]
        )
        
        # Update fixture
        fixtures.at[idx, "home_goals"] = home_goals
        fixtures.at[idx, "away_goals"] = away_goals
        fixtures.at[idx, "status"] = "completed"
        
        # Update league table
        # Home team
        home_idx = league_table[league_table["club_id"] == match["home_club_id"]].index[0]
        league_table.at[home_idx, "played"] += 1
        league_table.at[home_idx, "goals_for"] += home_goals
        league_table.at[home_idx, "goals_against"] += away_goals
        
        if home_goals > away_goals:
            league_table.at[home_idx, "won"] += 1
            league_table.at[home_idx, "home_wins"] += 1
            league_table.at[home_idx, "points"] += 3
            result_home = "W"
            result_away = "L"
        elif home_goals < away_goals:
            league_table.at[home_idx, "lost"] += 1
            league_table.at[home_idx, "home_losses"] += 1
            result_home = "L"
            result_away = "W"
        else:
            league_table.at[home_idx, "drawn"] += 1
            league_table.at[home_idx, "home_draws"] += 1
            league_table.at[home_idx, "points"] += 1
            result_home = "D"
            result_away = "D"
        
        # Away team
        away_idx = league_table[league_table["club_id"] == match["away_club_id"]].index[0]
        league_table.at[away_idx, "played"] += 1
        league_table.at[away_idx, "goals_for"] += away_goals
        league_table.at[away_idx, "goals_against"] += home_goals
        
        if away_goals > home_goals:
            league_table.at[away_idx, "won"] += 1
            league_table.at[away_idx, "away_wins"] += 1
            league_table.at[away_idx, "points"] += 3
        elif away_goals < home_goals:
            league_table.at[away_idx, "lost"] += 1
            league_table.at[away_idx, "away_losses"] += 1
        else:
            league_table.at[away_idx, "drawn"] += 1
            league_table.at[away_idx, "away_draws"] += 1
            league_table.at[away_idx, "points"] += 1
        
        # Update form (last 5 results)
        for team_idx, result in [(home_idx, result_home), (away_idx, result_away)]:
            current_form = league_table.at[team_idx, "form"]
            new_form = (current_form + result)[-5:]  # Keep last 5
            league_table.at[team_idx, "form"] = new_form
    
    # Calculate goal difference and sort table
    league_table["goal_difference"] = league_table["goals_for"] - league_table["goals_against"]
    league_table = league_table.sort_values(
        ["points", "goal_difference", "goals_for"],
        ascending=[False, False, False]
    ).reset_index(drop=True)
    
    # Assign positions
    league_table["position"] = range(1, len(league_table) + 1)
    
    return fixtures, league_table


if __name__ == "__main__":
    print("Match simulation module loaded.")