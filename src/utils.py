"""
Utility functions for Football Data Lab
Includes name generators, ID generators, and other helper functions
"""

import random
import numpy as np
from faker import Faker
from typing import Dict, List, Tuple
from src.config import NATIONALITIES, FANTASY_CITIES, CLUB_SUFFIXES, RANDOM_SEED

# Set random seeds for reproducibility
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Initialize Faker instances for different locales
fakers = {}
for nat in NATIONALITIES:
    fakers[nat["name"]] = Faker(nat["locale"])
    Faker.seed(RANDOM_SEED)


def generate_player_name(nationality: str) -> Dict[str, str]:
    """
    Generate a realistic player name based on nationality
    
    Args:
        nationality: Player's nationality
        
    Returns:
        Dictionary with first_name, last_name, and full_name
    """
    faker = fakers.get(nationality, Faker())
    
    try:
        first_name = faker.first_name_male()
        last_name = faker.last_name()
        
        # Check if names contain non-Latin characters
        # If they do, use romanized/English equivalents for problematic locales
        if not first_name.isascii() or not last_name.isascii():
            # Use name format that works with the locale
            if nationality == 'Chinese':
                # Use first_romanized_name if available, otherwise generic
                first_name = faker.first_romanized_name() if hasattr(faker, 'first_romanized_name') else f"Wei"
                last_name = faker.last_romanized_name() if hasattr(faker, 'last_romanized_name') else random.choice(['Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Huang', 'Zhao', 'Wu', 'Zhou'])
            elif nationality == 'Japanese':
                # Common Japanese names in romaji
                first_names = ['Takumi', 'Hiroshi', 'Kenji', 'Yuki', 'Ryo', 'Daiki', 'Kazuki', 'Haruto', 'Sota', 'Yuji']
                last_names = ['Tanaka', 'Suzuki', 'Takahashi', 'Watanabe', 'Ito', 'Yamamoto', 'Nakamura', 'Kobayashi', 'Kato', 'Yoshida']
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
            elif nationality == 'Korean':
                # Common Korean names in romaji
                first_names = ['Min-ho', 'Ji-woo', 'Seung-woo', 'Tae-yang', 'Joon-ho', 'Hyun-jin', 'Sung-min', 'Young-jae', 'Jin-woo', 'Ho-jin', 'Dong-hyun', 'Soo-hyun']
                last_names = ['Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Jang', 'Lim', 'Han', 'Oh', 'Seo', 'Shin']
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
            elif nationality in ['Egyptian', 'Saudi Arabian', 'Iranian', 'Moroccan', 'Algerian']:
                # Common Arabic/Middle Eastern names in Latin
                first_names = ['Mohamed', 'Ahmed', 'Ali', 'Omar', 'Hassan', 'Ibrahim', 'Youssef', 'Mahmoud', 'Karim', 'Mustafa', 'Tariq', 'Rashid', 'Samir', 'Hamza']
                last_names = ['Salah', 'Hassan', 'Ahmed', 'Mohamed', 'Ali', 'Ibrahim', 'Mahmoud', 'Abdel', 'El-Sayed', 'Farouk', 'Khalil', 'Nasser', 'Rashid', 'Amin']
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
            elif nationality == 'Russian':
                # Common Russian names in Latin/romanized
                first_names = ['Aleksandr', 'Dmitri', 'Ivan', 'Mikhail', 'Andrei', 'Nikolai', 'Sergei', 'Pavel', 'Viktor', 'Alexei', 'Yuri', 'Igor', 'Roman', 'Maxim']
                last_names = ['Ivanov', 'Petrov', 'Smirnov', 'Volkov', 'Sokolov', 'Kozlov', 'Popov', 'Vasiliev', 'Pavlov', 'Fedorov', 'Morozov', 'Novikov', 'Solovyov']
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
            elif nationality == 'Ukrainian':
                # Common Ukrainian names in Latin/romanized
                first_names = ['Oleksandr', 'Andriy', 'Viktor', 'Yuriy', 'Dmytro', 'Serhiy', 'Volodymyr', 'Oleh', 'Taras', 'Maksym', 'Ruslan', 'Pavlo', 'Bohdan']
                last_names = ['Shevchenko', 'Kovalenko', 'Bondarenko', 'Tkachenko', 'Koval', 'Melnyk', 'Petrenko', 'Moroz', 'Kravchenko', 'Lysenko', 'Marchenko', 'Sydorenko']
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
    except Exception:
        # Fallback to generic names if faker fails
        first_name = f"Player{random.randint(1, 9999)}"
        last_name = "Unknown"
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "full_name": f"{first_name} {last_name}"
    }


def generate_staff_name(nationality: str) -> Dict[str, str]:
    """
    Generate a realistic staff name based on nationality
    
    Args:
        nationality: Staff's nationality
        
    Returns:
        Dictionary with first_name, last_name, and full_name
    """
    return generate_player_name(nationality)


def select_nationality() -> str:
    """
    Randomly select a nationality based on weights
    
    Returns:
        Nationality name
    """
    nationalities = [nat["name"] for nat in NATIONALITIES]
    weights = [nat["weight"] for nat in NATIONALITIES]
    return random.choices(nationalities, weights=weights, k=1)[0]


def generate_club_name(city: str = None) -> Dict[str, str]:
    """
    Generate a fantasy club name
    
    Args:
        city: Optional city name, if None will select randomly
        
    Returns:
        Dictionary with city, suffix, full_name, and short_name
    """
    if city is None:
        city = random.choice(FANTASY_CITIES)
    
    suffix = random.choice(CLUB_SUFFIXES)
    full_name = f"{city} {suffix}"
    
    # Generate short name (e.g., "STW" for Stormwind United FC)
    if "FC" in suffix or "Athletic" in suffix:
        short_name = "".join([word[0] for word in city.split()]) + suffix.split()[0][:1]
    else:
        short_name = "".join([word[0] for word in city.split()]) + suffix[:3].upper()
    
    return {
        "city": city,
        "suffix": suffix,
        "full_name": full_name,
        "short_name": short_name[:4].upper()  # Max 4 characters
    }


def generate_stadium_name(city: str) -> str:
    """
    Generate a fantasy stadium name based on city
    
    Args:
        city: City name
        
    Returns:
        Stadium name
    """
    stadium_types = [
        "Arena", "Stadium", "Park", "Ground", "Field",
        "Dome", "Fortress", "Citadel", "Colosseum"
    ]
    
    descriptors = [
        "Thunder", "Lightning", "Storm", "Crystal", "Golden",
        "Silver", "Royal", "Imperial", "Grand", "Memorial",
        "Victory", "Glory", "Honor", "United", "Premier"
    ]
    
    # 50% chance to use city name, 50% chance to use descriptor
    if random.random() < 0.5:
        return f"{city} {random.choice(stadium_types)}"
    else:
        return f"{random.choice(descriptors)} {random.choice(stadium_types)}"


def generate_id(prefix: str, number: int) -> str:
    """
    Generate a unique ID with prefix
    
    Args:
        prefix: ID prefix (e.g., 'PLY' for player, 'CLB' for club)
        number: Sequential number
        
    Returns:
        Formatted ID string
    """
    return f"{prefix}_{number:05d}"


def calculate_overall_rating(attributes: Dict[str, float], position: str) -> float:
    """
    Calculate overall player rating based on position-specific attribute weights
    
    Args:
        attributes: Dictionary of player attributes
        position: Player position (GK, DEF, MID, FWD)
        
    Returns:
        Overall rating (0-100)
    """
    position_weights = {
        "GK": {
            "diving": 0.20, "handling": 0.20, "reflexes": 0.20,
            "positioning": 0.15, "kicking": 0.10, "concentration": 0.10, "decision_making": 0.05
        },
        "DEF": {
            "tackling": 0.20, "marking": 0.20, "positioning": 0.15,
            "heading": 0.15, "strength": 0.10, "pace": 0.10, "passing": 0.10
        },
        "MID": {
            "passing": 0.20, "ball_control": 0.18, "vision": 0.15,
            "stamina": 0.12, "dribbling": 0.12, "decision_making": 0.12, "tackling": 0.11
        },
        "FWD": {
            "shooting": 0.22, "finishing": 0.22, "positioning": 0.15,
            "pace": 0.15, "dribbling": 0.12, "ball_control": 0.10, "composure": 0.04
        }
    }
    
    weights = position_weights.get(position, position_weights["MID"])
    
    total = 0
    weight_sum = 0
    
    for attr, weight in weights.items():
        if attr in attributes:
            total += attributes[attr] * weight
            weight_sum += weight
    
    return round(total / weight_sum if weight_sum > 0 else 50, 1)


def calculate_market_value(
    overall_rating: float,
    age: int,
    potential: float,
    position: str
) -> int:
    """
    Calculate player market value based on various factors
    NOW WITH REALISTIC 2024/25 MARKET VALUES (up to £150M+)
    
    Args:
        overall_rating: Player's current overall rating
        age: Player's age
        potential: Player's potential rating
        position: Player's position
        
    Returns:
        Market value in currency units
    """
    # Base value from overall rating - MASSIVELY EXPANDED
    # Based on real 2024/25 market dynamics
    if overall_rating >= 90:
        # World-class superstars (Mbappe, Haaland, Vinicius level)
        base_value = overall_rating * 1_500_000  # £135M for 90 rating
    elif overall_rating >= 87:
        # Elite players (Salah, De Bruyne, Kane level)
        base_value = overall_rating * 1_200_000  # £104M for 87 rating
    elif overall_rating >= 85:
        # Top players (Saka, Foden, Rodri level)
        base_value = overall_rating * 900_000   # £76.5M for 85 rating
    elif overall_rating >= 82:
        # Very good players (Rice, Maddison level)
        base_value = overall_rating * 600_000   # £49.2M for 82 rating
    elif overall_rating >= 78:
        # Good players (regular starters for top clubs)
        base_value = overall_rating * 400_000   # £31.2M for 78 rating
    elif overall_rating >= 75:
        # Decent players (squad players, mid-table starters)
        base_value = overall_rating * 250_000   # £18.75M for 75 rating
    elif overall_rating >= 70:
        # Average players
        base_value = overall_rating * 150_000   # £10.5M for 70 rating
    else:
        # Below average
        base_value = overall_rating * 80_000    # £5.6M for 70 rating
    
    # Age multiplier - THE MOST IMPORTANT FACTOR
    if age < 20:
        # Wonderkids - HUGE potential premium
        potential_gap = potential - overall_rating
        if potential >= 85 and potential_gap >= 15:
            # Next Mbappe/Haaland
            age_multiplier = 2.0
        elif potential >= 80:
            # High potential young star
            age_multiplier = 1.6
        else:
            # Normal youth
            age_multiplier = 1.2
            
    elif 20 <= age <= 23:
        # Young stars establishing themselves
        potential_gap = potential - overall_rating
        if potential >= 85:
            # Future superstar (Bellingham type)
            age_multiplier = 1.8
        elif potential >= 80:
            # Strong potential
            age_multiplier = 1.5
        else:
            age_multiplier = 1.3
            
    elif 24 <= age <= 26:
        # PRIME YEARS - PEAK VALUE ZONE! (Liverpool's sweet spot)
        # Players entering their absolute peak
        age_multiplier = 1.7  # HIGHEST multiplier!
        
    elif 27 <= age <= 28:
        # Peak performance, still valuable
        age_multiplier = 1.5
        
    elif age == 29:
        # Last year of peak value
        age_multiplier = 1.2
        
    elif age == 30:
        # The cliff begins (but still good if elite)
        age_multiplier = 0.9
        
    elif age == 31:
        # Decline starts
        age_multiplier = 0.6
        
    elif age == 32:
        # Clear decline
        age_multiplier = 0.4
        
    elif age == 33:
        # Near end of career
        age_multiplier = 0.25
        
    else:
        # 34+ - Should be cheap (but United will still overpay!)
        age_multiplier = 0.15
    
    # Position multiplier - Attackers are EXPENSIVE
    position_multiplier = {
        "GK": 0.75,   # Keepers cheaper (Alisson £65M was exceptional)
        "DEF": 0.90,  # Defenders (Van Dijk £75M, Maguire £80M outlier)
        "MID": 1.10,  # Midfielders (Rice £105M, Enzo £107M)
        "FWD": 1.35   # Forwards MOST expensive (Haaland £51M+bonuses, Nunez £85M)
    }.get(position, 1.0)
    
    # Calculate base market value
    market_value = base_value * age_multiplier * position_multiplier
    
    # SPECIAL BONUSES
    
    # Superstar bonus (elite players command premium)
    if overall_rating >= 88 and age <= 28:
        market_value *= 1.3  # Superstar premium
    
    # Potential star bonus (young + high potential)
    if age <= 23 and potential >= 88:
        market_value *= 1.2  # Future star premium
    
    # Add market variance (+/- 15% for realism)
    # Real transfers have negotiation variance
    variance = random.uniform(0.85, 1.15)
    market_value = int(market_value * variance)
    
    # Set realistic floor and ceiling
    min_value = 300_000    # £300k minimum (youth/reserves)
    max_value = 200_000_000  # £200M ceiling (even Mbappe/Haaland capped here)
    
    market_value = max(min_value, min(max_value, int(market_value)))
    
    return market_value


# REAL-WORLD EXAMPLES FOR REFERENCE (2024/25 season):
# ============================================
# Jude Bellingham (20, 88 rating, CAM): ~£150M
# Erling Haaland (24, 91 rating, ST): ~£175M
# Kylian Mbappe (25, 91 rating, ST): ~£160M (free transfer but market value)
# Vinicius Jr (23, 89 rating, LW): ~£150M
# Mohamed Salah (32, 89 rating, RW): ~£50M (age factor!)
# Kevin De Bruyne (33, 88 rating, CAM): ~£30M (age factor!)
# Declan Rice (25, 84 rating, CDM): £105M actual transfer
# Enzo Fernandez (23, 83 rating, CM): £107M actual transfer
# Antony (24, 80 rating, RW): £85M (OVERPAID by United!)
# Harry Maguire (31, 78 rating, CB): £15M current value (was £80M!)


def calculate_weekly_wage(market_value: int, overall_rating: float) -> int:
    """
    Calculate player's weekly wage based on market value and rating
    
    Args:
        market_value: Player's market value
        overall_rating: Player's overall rating
        
    Returns:
        Weekly wage
    """
    # Rough formula: 0.5-1% of market value per year, divided by 52 weeks
    annual_wage = market_value * random.uniform(0.005, 0.01)
    weekly_wage = int(annual_wage / 52)
    
    # Ensure minimum wage
    min_wage = int(overall_rating * 100)
    
    return max(weekly_wage, min_wage)


def generate_date_of_birth(age: int, season: str = "2024/25") -> str:
    """
    Generate a date of birth for given age in the current season
    
    Args:
        age: Player's age
        season: Current season (format: "YYYY/YY")
        
    Returns:
        Date of birth string (YYYY-MM-DD)
    """
    season_year = int(season.split("/")[0])
    birth_year = season_year - age
    
    # Random month and day
    month = random.randint(1, 12)
    
    # Days in month
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = random.randint(1, days_in_month[month - 1])
    
    return f"{birth_year}-{month:02d}-{day:02d}"


def get_position_group(position: str) -> str:
    """
    Get position group from specific position
    
    Args:
        position: Specific position (e.g., 'CB', 'CAM')
        
    Returns:
        Position group ('GK', 'DEF', 'MID', 'FWD')
    """
    position_mapping = {
        "GK": "GK",
        "CB": "DEF", "LB": "DEF", "RB": "DEF", "LWB": "DEF", "RWB": "DEF",
        "CDM": "MID", "CM": "MID", "CAM": "MID", "LM": "MID", "RM": "MID",
        "LW": "FWD", "RW": "FWD", "ST": "FWD", "CF": "FWD"
    }
    return position_mapping.get(position, "MID")


def simulate_match_score(
    home_strength: float,
    away_strength: float,
    home_advantage: float = 0.15
) -> Tuple[int, int]:
    """
    Simulate a match score based on team strengths
    
    Args:
        home_strength: Home team average rating
        away_strength: Away team average rating
        home_advantage: Home advantage factor (default 0.15)
        
    Returns:
        Tuple of (home_goals, away_goals)
    """
    # Adjust for home advantage
    home_strength_adjusted = home_strength * (1 + home_advantage)
    
    # Calculate expected goals using Poisson distribution
    total_strength = home_strength_adjusted + away_strength
    home_xg = (home_strength_adjusted / total_strength) * 2.7  # Average 2.7 goals per match
    away_xg = (away_strength / total_strength) * 2.7
    
    # Sample from Poisson distribution
    home_goals = np.random.poisson(home_xg)
    away_goals = np.random.poisson(away_xg)
    
    return int(home_goals), int(away_goals)


def weighted_random_choice(items: List, weights: List):
    """
    Make a weighted random choice from items
    
    Args:
        items: List of items to choose from
        weights: List of weights corresponding to items
        
    Returns:
        Randomly selected item based on weights
    """
    return random.choices(items, weights=weights, k=1)[0]


def normalize_rating(rating: float, min_val: float = 0, max_val: float = 100) -> float:
    """
    Normalize a rating to be within specified range
    
    Args:
        rating: Rating to normalize
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Normalized rating
    """
    return max(min_val, min(max_val, rating))


def generate_form_rating(recent_results: List[str]) -> float:
    """
    Calculate form rating based on recent results
    
    Args:
        recent_results: List of recent results ('W', 'D', 'L')
        
    Returns:
        Form rating (1-10)
    """
    if not recent_results:
        return 5.0
    
    points = {"W": 3, "D": 1, "L": 0}
    total_points = sum(points[result] for result in recent_results)
    max_points = len(recent_results) * 3
    
    # Scale to 1-10
    form_rating = 1 + (total_points / max_points) * 9
    
    return round(form_rating, 1)