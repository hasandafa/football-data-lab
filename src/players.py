"""
Player generation module
Generates players with realistic attributes, ages, and positions
"""

import pandas as pd
import random
import numpy as np
from typing import Dict, List, Tuple
from src.config import (
    SQUAD_CONFIG,
    AGE_DISTRIBUTION,
    ATTRIBUTE_RANGES,
    RANDOM_SEED,
    CURRENT_SEASON
)
from src.utils import (
    generate_player_name,
    select_nationality,
    generate_id,
    calculate_overall_rating,
    calculate_market_value,
    calculate_weekly_wage,
    generate_date_of_birth,
    get_position_group,
    normalize_rating
)

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# Specific positions for each position group
POSITIONS = {
    "GK": ["GK"],
    "DEF": ["CB", "LB", "RB"],
    "MID": ["CDM", "CM", "CAM", "LM", "RM"],
    "FWD": ["LW", "RW", "ST"]
}


def determine_squad_composition() -> Dict[str, int]:
    """
    Determine how many players of each position group to generate
    
    Returns:
        Dictionary with counts for each position group
    """
    composition = {}
    for pos_group, config in SQUAD_CONFIG["positions"].items():
        composition[pos_group] = random.randint(config["min"], config["optimal"])
    
    return composition


def generate_age_based_on_distribution() -> int:
    """
    Generate player age based on configured distribution
    
    Returns:
        Player age
    """
    # Create age ranges and weights
    age_ranges = []
    weights = []
    
    for category, info in AGE_DISTRIBUTION.items():
        age_range = info["range"]
        weight = info["percentage"]
        # Add each year in range with equal sub-weight
        for age in range(age_range[0], age_range[1] + 1):
            age_ranges.append(age)
            weights.append(weight / (age_range[1] - age_range[0] + 1))
    
    return random.choices(age_ranges, weights=weights, k=1)[0]


def generate_physical_attributes(position_group: str, age: int) -> Dict[str, int]:
    """
    Generate physical attributes for a player
    
    Args:
        position_group: Position group (GK, DEF, MID, FWD)
        age: Player's age
        
    Returns:
        Dictionary of physical attributes
    """
    attr_ranges = ATTRIBUTE_RANGES[position_group]["physical"]
    
    attributes = {}
    for attr_name, (min_val, max_val) in attr_ranges.items():
        # Base attribute
        base_value = random.randint(min_val, max_val)
        
        # Age adjustment for physical attributes
        if age < 21:
            # Young players still developing physically
            adjustment = random.randint(-5, 0)
        elif 21 <= age <= 27:
            # Peak physical condition
            adjustment = random.randint(0, 3)
        elif 28 <= age <= 30:
            # Still peak
            adjustment = 0
        elif 31 <= age <= 33:
            # Beginning decline, especially pace
            if attr_name in ["pace", "stamina"]:
                adjustment = random.randint(-5, -2)
            else:
                adjustment = random.randint(-2, 0)
        else:
            # Clear decline
            if attr_name in ["pace", "stamina"]:
                adjustment = random.randint(-10, -5)
            else:
                adjustment = random.randint(-5, -2)
        
        attributes[attr_name] = int(normalize_rating(base_value + adjustment))
    
    return attributes


def generate_technical_attributes(position_group: str, age: int) -> Dict[str, int]:
    """
    Generate technical attributes for a player
    
    Args:
        position_group: Position group (GK, DEF, MID, FWD)
        age: Player's age
        
    Returns:
        Dictionary of technical attributes
    """
    attr_ranges = ATTRIBUTE_RANGES[position_group]["technical"]
    
    attributes = {}
    for attr_name, (min_val, max_val) in attr_ranges.items():
        base_value = random.randint(min_val, max_val)
        
        # Technical attributes improve with experience, decline slower
        if age < 21:
            adjustment = random.randint(-3, 0)
        elif 21 <= age <= 30:
            adjustment = random.randint(0, 2)
        elif 31 <= age <= 33:
            adjustment = 0
        else:
            adjustment = random.randint(-2, 0)
        
        attributes[attr_name] = int(normalize_rating(base_value + adjustment))
    
    return attributes


def generate_mental_attributes(position_group: str, age: int) -> Dict[str, int]:
    """
    Generate mental attributes for a player
    
    Args:
        position_group: Position group (GK, DEF, MID, FWD)
        age: Player's age
        
    Returns:
        Dictionary of mental attributes
    """
    attr_ranges = ATTRIBUTE_RANGES[position_group]["mental"]
    
    attributes = {}
    for attr_name, (min_val, max_val) in attr_ranges.items():
        base_value = random.randint(min_val, max_val)
        
        # Mental attributes improve with age/experience
        if age < 21:
            adjustment = random.randint(-5, 0)
        elif 21 <= age <= 25:
            adjustment = random.randint(0, 2)
        elif 26 <= age <= 32:
            adjustment = random.randint(2, 5)  # Peak mental attributes
        else:
            adjustment = random.randint(0, 3)  # Still good
        
        attributes[attr_name] = int(normalize_rating(base_value + adjustment))
    
    return attributes


def generate_player_potential(current_ability: float, age: int) -> float:
    """
    Generate player's potential ability based on current ability and age
    
    Args:
        current_ability: Player's current overall rating
        age: Player's age
        
    Returns:
        Potential ability rating
    """
    if age < 21:
        # Young players have higher potential growth
        potential = current_ability + random.uniform(10, 25)
    elif 21 <= age <= 24:
        potential = current_ability + random.uniform(5, 15)
    elif 25 <= age <= 27:
        potential = current_ability + random.uniform(2, 8)
    elif 28 <= age <= 29:
        potential = current_ability + random.uniform(0, 3)
    else:
        # Older players unlikely to improve much
        potential = current_ability + random.uniform(-5, 2)
    
    return normalize_rating(potential)


def select_specific_position(position_group: str) -> str:
    """
    Select a specific position within a position group
    
    Args:
        position_group: Position group (GK, DEF, MID, FWD)
        
    Returns:
        Specific position (e.g., 'CB', 'CAM', 'ST')
    """
    return random.choice(POSITIONS[position_group])


def select_secondary_positions(primary_position: str) -> List[str]:
    """
    Select 0-2 secondary positions for a player based on primary position
    
    Args:
        primary_position: Player's primary position
        
    Returns:
        List of secondary positions
    """
    # Position compatibility mapping
    compatible_positions = {
        "GK": [],  # Goalkeepers rarely play elsewhere
        "CB": ["RB", "LB", "CDM"],
        "LB": ["CB", "LWB", "LM"],
        "RB": ["CB", "RWB", "RM"],
        "CDM": ["CM", "CB"],
        "CM": ["CDM", "CAM", "RM", "LM"],
        "CAM": ["CM", "LW", "RW"],
        "LM": ["LW", "CM", "LB"],
        "RM": ["RW", "CM", "RB"],
        "LW": ["LM", "ST", "CAM"],
        "RW": ["RM", "ST", "CAM"],
        "ST": ["CF", "LW", "RW", "CAM"],
    }
    
    compatible = compatible_positions.get(primary_position, [])
    
    if not compatible:
        return []
    
    # 60% chance to have 1 secondary position, 20% for 2, 20% for none
    num_secondary = random.choices([0, 1, 2], weights=[0.2, 0.6, 0.2], k=1)[0]
    
    if num_secondary == 0:
        return []
    
    return random.sample(compatible, min(num_secondary, len(compatible)))


def generate_player(
    player_id: int,
    club_id: str,
    position_group: str,
    age: int = None,
    season: str = CURRENT_SEASON
) -> Dict:
    """
    Generate a complete player with all attributes
    
    Args:
        player_id: Unique player identifier number
        club_id: Club the player belongs to
        position_group: Position group (GK, DEF, MID, FWD)
        age: Player's age (if None, will be generated)
        season: Current season
        
    Returns:
        Dictionary containing all player information
    """
    # Generate age if not provided
    if age is None:
        age = generate_age_based_on_distribution()
    
    # Generate nationality and name
    nationality = select_nationality()
    name_info = generate_player_name(nationality)
    
    # Select positions
    primary_position = select_specific_position(position_group)
    secondary_positions = select_secondary_positions(primary_position)
    
    # Generate attributes
    physical_attrs = generate_physical_attributes(position_group, age)
    technical_attrs = generate_technical_attributes(position_group, age)
    mental_attrs = generate_mental_attributes(position_group, age)
    
    # Combine all attributes
    all_attributes = {**physical_attrs, **technical_attrs, **mental_attrs}
    
    # Calculate overall rating
    overall_rating = calculate_overall_rating(all_attributes, position_group)
    
    # Generate potential
    potential = generate_player_potential(overall_rating, age)
    
    # Physical characteristics
    height_ranges = {
        "GK": (185, 200),
        "DEF": (178, 195),
        "MID": (170, 185),
        "FWD": (170, 190)
    }
    height = random.randint(*height_ranges[position_group])
    weight = int(height * random.uniform(0.38, 0.44))  # Realistic weight for height
    
    # Preferred foot
    preferred_foot = random.choices(
        ["Right", "Left", "Both"],
        weights=[0.70, 0.25, 0.05],
        k=1
    )[0]
    
    # Calculate market value and wage
    market_value = calculate_market_value(overall_rating, age, potential, position_group)
    weekly_wage = calculate_weekly_wage(market_value, overall_rating)
    
    # Contract (1-5 years remaining)
    contract_years = random.randint(1, 5)
    
    # Generate date of birth
    date_of_birth = generate_date_of_birth(age, season)
    
    # Form and condition (for active players)
    current_form = round(random.uniform(5.0, 8.5), 1)
    fitness_level = random.randint(85, 100)
    morale = random.randint(12, 18)
    
    # Personality traits
    leadership = random.randint(1, 20)
    professionalism = random.randint(1, 20)
    temperament = random.choice(["Calm", "Balanced", "Aggressive"])
    consistency = random.randint(1, 20)
    injury_proneness = random.randint(1, 20)  # Higher = more injury prone
    
    # Career stats (will be 0 for newly generated players, updated during simulation)
    career_stats = {
        "appearances": 0,
        "goals": 0,
        "assists": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "clean_sheets": 0 if position_group in ["GK", "DEF"] else None,
    }
    
    # Compile player data
    player_data = {
        "player_id": generate_id("PLY", player_id),
        "club_id": club_id,
        "first_name": name_info["first_name"],
        "last_name": name_info["last_name"],
        "full_name": name_info["full_name"],
        "nationality": nationality,
        "date_of_birth": date_of_birth,
        "age": age,
        "height_cm": height,
        "weight_kg": weight,
        "preferred_foot": preferred_foot,
        
        # Positions
        "position_group": position_group,
        "primary_position": primary_position,
        "secondary_positions": ",".join(secondary_positions) if secondary_positions else None,
        
        # Ratings
        "overall_rating": overall_rating,
        "potential": potential,
        
        # Physical attributes
        **{f"phys_{k}": v for k, v in physical_attrs.items()},
        
        # Technical attributes
        **{f"tech_{k}": v for k, v in technical_attrs.items()},
        
        # Mental attributes
        **{f"mental_{k}": v for k, v in mental_attrs.items()},
        
        # Contract and financial
        "contract_years_remaining": contract_years,
        "market_value": market_value,
        "weekly_wage": weekly_wage,
        
        # Form and condition
        "current_form": current_form,
        "fitness_level": fitness_level,
        "morale": morale,
        "injury_status": "Healthy",
        
        # Personality
        "leadership": leadership,
        "professionalism": professionalism,
        "temperament": temperament,
        "consistency": consistency,
        "injury_proneness": injury_proneness,
        
        # Career stats
        **{f"career_{k}": v for k, v in career_stats.items()},
    }
    
    return player_data


def generate_squad(club_id: str, club_tier: str, season: str = CURRENT_SEASON) -> pd.DataFrame:
    """
    Generate a complete squad for a club
    
    Args:
        club_id: Club identifier
        club_tier: Club tier (affects player quality)
        season: Current season
        
    Returns:
        DataFrame containing all players in the squad
    """
    squad_composition = determine_squad_composition()
    players = []
    player_counter = 1
    
    # Adjust overall rating ranges based on club tier
    tier_adjustments = {
        "top_tier": 8,
        "mid_tier": 0,
        "lower_tier": -8
    }
    adjustment = tier_adjustments.get(club_tier, 0)
    
    for pos_group, count in squad_composition.items():
        for _ in range(count):
            player_data = generate_player(player_counter, club_id, pos_group, season=season)
            
            # Adjust ratings based on club tier
            player_data["overall_rating"] = normalize_rating(
                player_data["overall_rating"] + adjustment
            )
            player_data["potential"] = normalize_rating(
                player_data["potential"] + adjustment
            )
            
            # Recalculate market value with adjusted rating
            player_data["market_value"] = calculate_market_value(
                player_data["overall_rating"],
                player_data["age"],
                player_data["potential"],
                pos_group
            )
            player_data["weekly_wage"] = calculate_weekly_wage(
                player_data["market_value"],
                player_data["overall_rating"]
            )
            
            players.append(player_data)
            player_counter += 1
    
    squad_df = pd.DataFrame(players)
    
    # Assign jersey numbers (1-99)
    # GK typically get 1, 12, 13
    # Others get numbers based on position
    jersey_numbers = list(range(1, 100))
    random.shuffle(jersey_numbers)
    squad_df["jersey_number"] = jersey_numbers[:len(squad_df)]
    
    # Ensure GK gets appropriate numbers
    gk_numbers = [1, 12, 13, 22, 25]
    gk_indices = squad_df[squad_df["position_group"] == "GK"].index
    for i, idx in enumerate(gk_indices):
        if i < len(gk_numbers):
            squad_df.at[idx, "jersey_number"] = gk_numbers[i]
    
    return squad_df


if __name__ == "__main__":
    # Test player generation
    print("Generating a test player...")
    test_player = generate_player(1, "CLB_00001", "MID", age=24)
    print(f"\nPlayer: {test_player['full_name']}")
    print(f"Position: {test_player['primary_position']} ({test_player['position_group']})")
    print(f"Age: {test_player['age']}, Nationality: {test_player['nationality']}")
    print(f"Overall: {test_player['overall_rating']}, Potential: {test_player['potential']}")
    print(f"Market Value: ${test_player['market_value']:,}")
    print(f"Weekly Wage: ${test_player['weekly_wage']:,}")
    
    print("\n\nGenerating a test squad...")
    test_squad = generate_squad("CLB_00001", "top_tier")
    print(f"Squad size: {len(test_squad)}")
    print("\nPosition distribution:")
    print(test_squad["position_group"].value_counts())
    print("\nTop 5 players by overall rating:")
    print(test_squad.nlargest(5, "overall_rating")[
        ["full_name", "primary_position", "age", "overall_rating", "potential"]
    ])