"""
Club generation module
Generates clubs with all necessary attributes
"""

import pandas as pd
import random
from typing import List
from src.config import (
    LEAGUE_CONFIG,
    FANTASY_CITIES,
    STADIUM_CAPACITY,
    CLUB_BUDGET,
    RANDOM_SEED
)
from src.utils import generate_club_name, generate_stadium_name, generate_id

random.seed(RANDOM_SEED)


def assign_club_tier(position: int, total_clubs: int) -> str:
    """
    Assign club tier based on their position in the league
    
    Args:
        position: Club's position (1-indexed)
        total_clubs: Total number of clubs
        
    Returns:
        Club tier ('top_tier', 'mid_tier', 'lower_tier')
    """
    if position <= total_clubs * 0.25:  # Top 25%
        return "top_tier"
    elif position <= total_clubs * 0.70:  # Next 45%
        return "mid_tier"
    else:  # Bottom 30%
        return "lower_tier"


def generate_clubs(num_clubs: int = None) -> pd.DataFrame:
    """
    Generate all clubs for the league
    
    Args:
        num_clubs: Number of clubs to generate (default from config)
        
    Returns:
        DataFrame containing all club information
    """
    if num_clubs is None:
        num_clubs = LEAGUE_CONFIG["num_teams"]
    
    clubs_data = []
    used_cities = []
    
    for i in range(num_clubs):
        # Select unique city
        available_cities = [city for city in FANTASY_CITIES if city not in used_cities]
        city = random.choice(available_cities)
        used_cities.append(city)
        
        # Generate club name
        club_info = generate_club_name(city)
        
        # Assign tier (distribute evenly at first)
        tier = assign_club_tier(i + 1, num_clubs)
        
        # Generate stadium
        stadium_name = generate_stadium_name(city)
        stadium_capacity = random.randint(
            STADIUM_CAPACITY[tier]["min"],
            STADIUM_CAPACITY[tier]["max"]
        )
        
        # Generate budget
        annual_budget = random.randint(
            CLUB_BUDGET[tier]["min"],
            CLUB_BUDGET[tier]["max"]
        )
        
        # Club colors
        colors = [
            ("Red", "White"), ("Blue", "White"), ("Green", "White"),
            ("Yellow", "Black"), ("Black", "White"), ("Purple", "Gold"),
            ("Orange", "Blue"), ("Maroon", "Sky Blue"), ("Navy", "Red"),
            ("Crimson", "Silver")
        ]
        primary_color, secondary_color = random.choice(colors)
        
        # Founded year (between 1880 and 2010)
        founded_year = random.randint(1880, 2010)
        
        # Reputation (1-100, higher for top tier)
        reputation_ranges = {
            "top_tier": (75, 95),
            "mid_tier": (50, 74),
            "lower_tier": (30, 49)
        }
        reputation = random.randint(*reputation_ranges[tier])
        
        # Facilities quality (1-20, higher for top tier)
        facility_ranges = {
            "top_tier": (15, 20),
            "mid_tier": (10, 14),
            "lower_tier": (5, 9)
        }
        training_facility = random.randint(*facility_ranges[tier])
        youth_academy_rating = random.randint(*facility_ranges[tier])
        
        # Playing style
        formations = ["4-3-3", "4-4-2", "4-2-3-1", "3-5-2", "4-1-4-1", "3-4-3"]
        playing_styles = [
            "Possession", "Counter-Attack", "High Pressing", 
            "Defensive", "Balanced", "Direct"
        ]
        
        club_data = {
            "club_id": generate_id("CLB", i + 1),
            "full_name": club_info["full_name"],
            "short_name": club_info["short_name"],
            "city": club_info["city"],
            "tier": tier,
            "founded_year": founded_year,
            "stadium_name": stadium_name,
            "stadium_capacity": stadium_capacity,
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "annual_budget_millions": annual_budget,
            "reputation": reputation,
            "training_facility_rating": training_facility,
            "youth_academy_rating": youth_academy_rating,
            "preferred_formation": random.choice(formations),
            "playing_style": random.choice(playing_styles),
        }
        
        clubs_data.append(club_data)
    
    df = pd.DataFrame(clubs_data)
    
    # Sort by reputation initially (top clubs first)
    df = df.sort_values("reputation", ascending=False).reset_index(drop=True)
    
    return df


def generate_club_staff(club_id: str, club_tier: str) -> pd.DataFrame:
    """
    Generate staff for a club (manager and coaching staff)
    
    Args:
        club_id: Club identifier
        club_tier: Club tier level
        
    Returns:
        DataFrame with club staff information
    """
    from src.utils import generate_staff_name, select_nationality, generate_id
    
    staff_data = []
    
    # Manager
    manager_nationality = select_nationality()
    manager_name = generate_staff_name(manager_nationality)
    manager_age = random.randint(35, 70)
    
    # Manager quality based on club tier
    quality_ranges = {
        "top_tier": (15, 20),
        "mid_tier": (10, 14),
        "lower_tier": (5, 9)
    }
    
    manager = {
        "staff_id": generate_id("STF", 1),
        "club_id": club_id,
        "role": "Manager",
        "first_name": manager_name["first_name"],
        "last_name": manager_name["last_name"],
        "full_name": manager_name["full_name"],
        "nationality": manager_nationality,
        "age": manager_age,
        "tactical_rating": random.randint(*quality_ranges[club_tier]),
        "man_management_rating": random.randint(*quality_ranges[club_tier]),
        "contract_years": random.randint(2, 4),
    }
    staff_data.append(manager)
    
    # Assistant coaches
    staff_roles = [
        "Assistant Coach",
        "Goalkeeping Coach",
        "Fitness Coach",
        "Set Piece Coach"
    ]
    
    staff_counter = 2
    for role in staff_roles:
        nationality = select_nationality()
        name = generate_staff_name(nationality)
        
        staff_member = {
            "staff_id": generate_id("STF", staff_counter),
            "club_id": club_id,
            "role": role,
            "first_name": name["first_name"],
            "last_name": name["last_name"],
            "full_name": name["full_name"],
            "nationality": nationality,
            "age": random.randint(30, 65),
            "specialization_rating": random.randint(*quality_ranges[club_tier]),
            "contract_years": random.randint(1, 3),
        }
        staff_data.append(staff_member)
        staff_counter += 1
    
    return pd.DataFrame(staff_data)


if __name__ == "__main__":
    # Test club generation
    print("Generating clubs...")
    clubs = generate_clubs()
    print(f"\nGenerated {len(clubs)} clubs:")
    print(clubs[["full_name", "city", "tier", "reputation"]].head(10))
    
    print("\n\nGenerating staff for first club...")
    first_club = clubs.iloc[0]
    staff = generate_club_staff(first_club["club_id"], first_club["tier"])
    print(staff[["full_name", "role", "nationality", "age"]])