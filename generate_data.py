"""
Football Data Lab - Main Data Generation Script

This script generates all synthetic football data including:
- Leagues and seasons
- Clubs and stadiums
- Players and staff
- Youth academies
- Matches and results
- Transfer history

Run this script to generate a complete 5-season dataset.
"""

import os
import sys
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import (
    SEASONS,
    RAW_DATA_DIR,
    LEAGUE_CONFIG,
    CURRENT_SEASON
)
from src.leagues import generate_league, generate_season_info
from src.clubs import generate_clubs
from src.players import generate_squad
from src.staff import generate_all_staff
from src.youth_academy import generate_youth_academy_players
from src.matches import generate_season_fixtures, simulate_season_matches
from src.transfers import create_initial_transfer_history


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def save_dataframe(df, filename, description):
    """Save DataFrame to CSV and print info"""
    filepath = RAW_DATA_DIR / filename
    df.to_csv(filepath, index=False)
    print(f"✓ {description}: {len(df)} records → {filename}")
    return filepath


def generate_all_data():
    """
    Main function to generate all football data
    """
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                   FOOTBALL DATA LAB                                 ║")
    print("║              Synthetic Football Data Generator                      ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    start_time = datetime.now()
    
    # ===== STEP 1: Generate League and Season Information =====
    print_header("STEP 1: Generating League and Season Information")
    
    league_info = generate_league()
    print(f"✓ League: {league_info['name']} ({league_info['short_name']})")
    print(f"  Teams: {league_info['num_teams']}")
    print(f"  Country: {league_info['country']}")
    
    seasons_df = generate_season_info()
    print(f"✓ Seasons: {len(seasons_df)} seasons from {SEASONS[0]} to {SEASONS[-1]}")
    
    # Save league info
    league_df = pd.DataFrame([league_info])
    save_dataframe(league_df, "league_info.csv", "League information")
    save_dataframe(seasons_df, "seasons.csv", "Season information")
    
    # ===== STEP 2: Generate Clubs =====
    print_header("STEP 2: Generating Clubs")
    
    clubs_df = generate_clubs(LEAGUE_CONFIG["num_teams"])
    print(f"✓ Generated {len(clubs_df)} clubs")
    print(f"  Top tier: {len(clubs_df[clubs_df['tier'] == 'top_tier'])}")
    print(f"  Mid tier: {len(clubs_df[clubs_df['tier'] == 'mid_tier'])}")
    print(f"  Lower tier: {len(clubs_df[clubs_df['tier'] == 'lower_tier'])}")
    
    save_dataframe(clubs_df, "clubs.csv", "Clubs")
    
    # ===== STEP 3: Generate Staff =====
    print_header("STEP 3: Generating Club Staff")
    
    all_staff_df = generate_all_staff(clubs_df)
    print(f"✓ Generated {len(all_staff_df)} staff members")
    print(f"  Managers: {len(all_staff_df[all_staff_df['role'] == 'Manager'])}")
    print(f"  Coaching staff: {len(all_staff_df[all_staff_df['role'] != 'Manager'])}")
    
    save_dataframe(all_staff_df, "staff.csv", "Club staff")
    
    # ===== STEP 4: Generate Players =====
    print_header("STEP 4: Generating Players for All Clubs")
    
    all_players = []
    player_id_counter = 1
    
    print("\nGenerating squads...")
    for idx, club in clubs_df.iterrows():
        squad = generate_squad(club["club_id"], club["tier"], CURRENT_SEASON)
        
        # Reassign player IDs to be unique across all clubs
        for i, player_idx in enumerate(squad.index):
            squad.at[player_idx, "player_id"] = f"PLY_{player_id_counter:05d}"
            player_id_counter += 1
        
        all_players.append(squad)
        
        if (idx + 1) % 5 == 0:
            print(f"  Progress: {idx + 1}/{len(clubs_df)} clubs")
    
    all_players_df = pd.concat(all_players, ignore_index=True)
    
    print(f"\n✓ Generated {len(all_players_df)} players")
    print(f"  Goalkeepers: {len(all_players_df[all_players_df['position_group'] == 'GK'])}")
    print(f"  Defenders: {len(all_players_df[all_players_df['position_group'] == 'DEF'])}")
    print(f"  Midfielders: {len(all_players_df[all_players_df['position_group'] == 'MID'])}")
    print(f"  Forwards: {len(all_players_df[all_players_df['position_group'] == 'FWD'])}")
    print(f"  Average overall rating: {all_players_df['overall_rating'].mean():.1f}")
    
    save_dataframe(all_players_df, "players.csv", "Players")
    
    # ===== STEP 5: Generate Youth Academies =====
    print_header("STEP 5: Generating Youth Academy Players")
    
    all_youth = []
    youth_id_counter = 50000  # Start youth IDs from 50000
    
    for club in clubs_df.itertuples():
        youth_players = generate_youth_academy_players(
            club.club_id,
            season=CURRENT_SEASON
        )
        
        # Reassign youth player IDs
        for i, player_idx in enumerate(youth_players.index):
            youth_players.at[player_idx, "player_id"] = f"PLY_{youth_id_counter:05d}"
            youth_id_counter += 1
        
        all_youth.append(youth_players)
    
    all_youth_df = pd.concat(all_youth, ignore_index=True)
    
    print(f"✓ Generated {len(all_youth_df)} youth academy players")
    print(f"  Average age: {all_youth_df['age'].mean():.1f}")
    print(f"  Average potential: {all_youth_df['potential'].mean():.1f}")
    
    save_dataframe(all_youth_df, "youth_academy.csv", "Youth academy players")
    
    # ===== STEP 6: Generate Matches for Current Season =====
    print_header("STEP 6: Generating and Simulating Matches")
    
    print(f"\nGenerating fixtures for {CURRENT_SEASON}...")
    fixtures_df = generate_season_fixtures(clubs_df, CURRENT_SEASON)
    print(f"✓ Generated {len(fixtures_df)} fixtures")
    
    print(f"\nSimulating matches...")
    simulated_fixtures, league_table = simulate_season_matches(
        fixtures_df,
        clubs_df,
        all_players_df
    )
    
    print(f"✓ Simulated {len(simulated_fixtures)} matches")
    print(f"\nFinal League Table ({CURRENT_SEASON}):")
    print(league_table[["position", "club_name", "played", "won", "drawn", "lost", "points"]].head(5))
    print("...")
    print(league_table[["position", "club_name", "played", "won", "drawn", "lost", "points"]].tail(3))
    
    save_dataframe(simulated_fixtures, f"matches_{CURRENT_SEASON.replace('/', '_')}.csv", f"Matches {CURRENT_SEASON}")
    save_dataframe(league_table, f"league_table_{CURRENT_SEASON.replace('/', '_')}.csv", f"League table {CURRENT_SEASON}")
    
    # ===== STEP 7: Generate Transfer History =====
    print_header("STEP 7: Generating Transfer History")
    
    transfers_df = create_initial_transfer_history(
        all_players_df,
        clubs_df,
        SEASONS
    )
    
    if not transfers_df.empty:
        print(f"✓ Generated {len(transfers_df)} historical transfers")
        save_dataframe(transfers_df, "transfer_history.csv", "Transfer history")
    else:
        print("✓ No historical transfers (initial dataset)")
    
    # ===== SUMMARY =====
    print_header("DATA GENERATION COMPLETE!")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n📊 Dataset Summary:")
    print(f"   • Clubs: {len(clubs_df)}")
    print(f"   • Staff: {len(all_staff_df)}")
    print(f"   • Players: {len(all_players_df)}")
    print(f"   • Youth Players: {len(all_youth_df)}")
    print(f"   • Matches: {len(simulated_fixtures)}")
    print(f"   • Transfers: {len(transfers_df) if not transfers_df.empty else 0}")
    
    print(f"\n⏱️  Generation time: {duration:.2f} seconds")
    print(f"\n💾 All data saved to: {RAW_DATA_DIR}")
    
    print("\n" + "=" * 70)
    print("  Next steps:")
    print("  1. Check the data folder for generated CSV files")
    print("  2. Run Jupyter notebooks for analysis")
    print("  3. Launch Streamlit dashboard for visualization")
    print("=" * 70 + "\n")
    
    return {
        "clubs": clubs_df,
        "players": all_players_df,
        "youth": all_youth_df,
        "staff": all_staff_df,
        "matches": simulated_fixtures,
        "league_table": league_table,
        "transfers": transfers_df
    }


if __name__ == "__main__":
    try:
        data = generate_all_data()
        print("✅ Success! Data generation completed without errors.\n")
    except Exception as e:
        print(f"\n❌ Error during data generation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)