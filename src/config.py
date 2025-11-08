"""
Configuration file for Football Data Lab
Contains all settings for data generation, league structure, and simulation parameters
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Seasons to generate
START_SEASON = "2020/21"
END_SEASON = "2024/25"
SEASONS = [
    "2020/21",
    "2021/22", 
    "2022/23",
    "2023/24",
    "2024/25"
]
CURRENT_SEASON = "2024/25"

# League configuration
LEAGUE_CONFIG = {
    "name": "Ironforge Premier League",
    "short_name": "IPL",
    "country": "Aetheria",
    "num_teams": 20,
    "matches_per_season": 38,  # Each team plays 38 matches (home and away)
    "promotion_spots": 3,
    "relegation_spots": 3,
    "european_spots": 4,  # Top 4 qualify for continental competition
}

# Squad configuration
SQUAD_CONFIG = {
    "min_squad_size": 23,
    "max_squad_size": 30,
    "optimal_squad_size": 27,
    "positions": {
        "GK": {"min": 2, "max": 3, "optimal": 3},
        "DEF": {"min": 7, "max": 10, "optimal": 9},
        "MID": {"min": 7, "max": 10, "optimal": 9},
        "FWD": {"min": 5, "max": 8, "optimal": 6},
    }
}

# Player age distribution (for initial squad generation)
AGE_DISTRIBUTION = {
    "youth_prospects": {"range": (16, 20), "percentage": 0.20},
    "young_players": {"range": (21, 24), "percentage": 0.25},
    "prime_age": {"range": (25, 29), "percentage": 0.40},
    "experienced": {"range": (30, 33), "percentage": 0.12},
    "veterans": {"range": (34, 38), "percentage": 0.03},
}

# Youth academy configuration
YOUTH_ACADEMY_CONFIG = {
    "players_per_season": 5,  # New youth players generated each season
    "age_range": (16, 17),
    "promotion_age": 18,
    "min_ability_for_promotion": 55,
    "min_potential_for_promotion": 65,
    "annual_promotions_target": (1, 3),  # Min and max promotions per club per season
}

# Player development rates (ability change per season by age)
DEVELOPMENT_RATES = {
    "16-21": {"min": 4, "max": 8},  # Rapid development
    "22-27": {"min": 2, "max": 5},  # Growth phase
    "28-30": {"min": -1, "max": 2},  # Peak/stable
    "31-33": {"min": -2, "max": -1},  # Early decline
    "34+": {"min": -4, "max": -2},  # Clear decline
}

# Retirement probabilities by age
RETIREMENT_PROBS = {
    34: 0.10,
    35: 0.20,
    36: 0.40,
    37: 0.60,
    38: 0.80,
    39: 0.95,
}

# Transfer configuration
TRANSFER_CONFIG = {
    "summer_window": {
        "start_month": 6,
        "end_month": 8,
        "transfer_percentage": 0.65,  # 65% of transfers happen in summer
    },
    "winter_window": {
        "start_month": 1,
        "end_month": 1,
        "transfer_percentage": 0.35,  # 35% of transfers happen in winter
    },
    "transfers_per_club_per_season": {
        "incoming": {"min": 3, "max": 8},
        "outgoing": {"min": 3, "max": 8},
    },
    "free_transfer_ratio": 0.20,  # 20% of transfers are free
    "loan_ratio": 0.15,  # 15% of transfers are loans
}

# Player attributes ranges (1-100 scale)
ATTRIBUTE_RANGES = {
    "GK": {
        "physical": {"pace": (30, 60), "strength": (50, 85), "stamina": (60, 90)},
        "technical": {
            "diving": (40, 95),
            "handling": (40, 95),
            "kicking": (30, 85),
            "reflexes": (40, 95),
            "positioning": (40, 90),
        },
        "mental": {
            "concentration": (40, 90),
            "decision_making": (40, 85),
            "leadership": (30, 90),
        }
    },
    "DEF": {
        "physical": {"pace": (40, 85), "strength": (60, 95), "stamina": (60, 90)},
        "technical": {
            "tackling": (50, 95),
            "marking": (50, 95),
            "heading": (50, 95),
            "passing": (40, 85),
            "ball_control": (35, 80),
        },
        "mental": {
            "positioning": (50, 95),
            "concentration": (50, 90),
            "decision_making": (40, 85),
        }
    },
    "MID": {
        "physical": {"pace": (50, 90), "strength": (45, 80), "stamina": (65, 95)},
        "technical": {
            "passing": (50, 95),
            "ball_control": (50, 95),
            "dribbling": (45, 90),
            "shooting": (35, 85),
            "tackling": (35, 85),
        },
        "mental": {
            "vision": (45, 95),
            "decision_making": (50, 90),
            "work_rate": (50, 95),
        }
    },
    "FWD": {
        "physical": {"pace": (60, 95), "strength": (45, 90), "stamina": (55, 90)},
        "technical": {
            "shooting": (50, 95),
            "finishing": (50, 95),
            "dribbling": (50, 95),
            "ball_control": (50, 90),
            "heading": (40, 85),
        },
        "mental": {
            "positioning": (50, 95),
            "composure": (45, 90),
            "decision_making": (40, 85),
        }
    }
}

# Match simulation parameters
MATCH_CONFIG = {
    "home_advantage": 0.15,  # 15% boost to home team performance
    "goals_per_match_avg": 2.7,
    "possession_variance": 0.20,
    "injury_probability": 0.05,  # 5% chance of injury per match per player
    "yellow_card_probability": 0.15,
    "red_card_probability": 0.02,
}

# Stadium capacity ranges by club tier
STADIUM_CAPACITY = {
    "top_tier": {"min": 45000, "max": 75000},
    "mid_tier": {"min": 25000, "max": 44999},
    "lower_tier": {"min": 15000, "max": 24999},
}

# Club budget ranges (annual, in millions)
CLUB_BUDGET = {
    "top_tier": {"min": 150, "max": 300},
    "mid_tier": {"min": 50, "max": 149},
    "lower_tier": {"min": 20, "max": 49},
}

# Nationalities for name generation (will be used with Faker)
NATIONALITIES = [
    # Major European Powers (Top football nations)
    {"name": "English", "weight": 0.185, "locale": "en_GB"},
    {"name": "Spanish", "weight": 0.12, "locale": "es_ES"},
    {"name": "French", "weight": 0.11, "locale": "fr_FR"},
    {"name": "German", "weight": 0.10, "locale": "de_DE"},
    {"name": "Italian", "weight": 0.08, "locale": "it_IT"},
    {"name": "Portuguese", "weight": 0.05, "locale": "pt_PT"},
    {"name": "Dutch", "weight": 0.05, "locale": "nl_NL"},
    {"name": "Belgian", "weight": 0.04, "locale": "nl_BE"},
    
    # South American Powers
    {"name": "Brazilian", "weight": 0.09, "locale": "pt_BR"},
    {"name": "Argentine", "weight": 0.07, "locale": "es_AR"},
    {"name": "Colombian", "weight": 0.03, "locale": "es_ES"},
    {"name": "Uruguayan", "weight": 0.02, "locale": "es_ES"},
    {"name": "Chilean", "weight": 0.015, "locale": "es_ES"},
    
    # Eastern/Central Europe
    {"name": "Croatian", "weight": 0.025, "locale": "hr_HR"},
    {"name": "Serbian", "weight": 0.020, "locale": "en_GB"},
    {"name": "Polish", "weight": 0.020, "locale": "pl_PL"},
    {"name": "Czech", "weight": 0.015, "locale": "cs_CZ"},
    {"name": "Ukrainian", "weight": 0.015, "locale": "uk_UA"},
    {"name": "Russian", "weight": 0.015, "locale": "ru_RU"},
    {"name": "Romanian", "weight": 0.010, "locale": "ro_RO"},
    
    # Nordic Countries
    {"name": "Swedish", "weight": 0.015, "locale": "sv_SE"},
    {"name": "Danish", "weight": 0.012, "locale": "da_DK"},
    {"name": "Norwegian", "weight": 0.010, "locale": "no_NO"},
    
    # Other European
    {"name": "Turkish", "weight": 0.020, "locale": "tr_TR"},
    {"name": "Austrian", "weight": 0.010, "locale": "de_AT"},
    {"name": "Swiss", "weight": 0.010, "locale": "de_CH"},
    {"name": "Greek", "weight": 0.008, "locale": "el_GR"},
    {"name": "Irish", "weight": 0.008, "locale": "en_IE"},
    {"name": "Scottish", "weight": 0.008, "locale": "en_GB"},
    {"name": "Welsh", "weight": 0.005, "locale": "en_GB"},
    
    # African Nations (Using fallback locales)
    {"name": "Nigerian", "weight": 0.025, "locale": "en_GB"},
    {"name": "Senegalese", "weight": 0.020, "locale": "fr_FR"},
    {"name": "Ivorian", "weight": 0.018, "locale": "fr_FR"},
    {"name": "Ghanaian", "weight": 0.015, "locale": "en_GB"},
    {"name": "Cameroonian", "weight": 0.015, "locale": "fr_FR"},
    {"name": "Egyptian", "weight": 0.015, "locale": "ar_EG"},
    {"name": "Moroccan", "weight": 0.012, "locale": "ar_EG"},
    {"name": "Algerian", "weight": 0.010, "locale": "ar_EG"},
    {"name": "South African", "weight": 0.008, "locale": "en_GB"},  # Use English
    {"name": "Malian", "weight": 0.008, "locale": "fr_FR"},
    
    # Asian Nations
    {"name": "Japanese", "weight": 0.026, "locale": "ja_JP"},
    {"name": "Korean", "weight": 0.021, "locale": "ko_KR"},
    {"name": "Indonesian", "weight": 0.018, "locale": "id_ID"},  # 🇮🇩
    {"name": "Australian", "weight": 0.012, "locale": "en_AU"},
    {"name": "Iranian", "weight": 0.010, "locale": "fa_IR"},
    {"name": "Saudi Arabian", "weight": 0.015, "locale": "ar_SA"},
    {"name": "Chinese", "weight": 0.007, "locale": "zh_CN"},
    
    # North/Central America
    {"name": "Mexican", "weight": 0.015, "locale": "es_MX"},
    {"name": "American", "weight": 0.012, "locale": "en_US"},
    {"name": "Canadian", "weight": 0.008, "locale": "en_CA"},
    
    # Other South American
    {"name": "Ecuadorian", "weight": 0.008, "locale": "es_ES"},
    {"name": "Peruvian", "weight": 0.006, "locale": "es_ES"},
    {"name": "Paraguayan", "weight": 0.005, "locale": "es_ES"},
    {"name": "Venezuelan", "weight": 0.005, "locale": "es_ES"},
]

# Fantasy city names for clubs
FANTASY_CITIES = [
    "Stormwind", "Krondor", "Silverpeak", "Moonlight Bay", "Thunder Valley",
    "Crystal Coast", "Shadow Harbor", "Golden Plains", "Frost Ridge", "Emerald Hills",
    "Crimson Port", "Azure Bay", "Sunset Shore", "Dragon's Keep", "Phoenix Rise",
    "Silver Falls", "Granite City", "Maple Grove", "Riverside", "Oakmont",
    "Pinewood", "Cedarville", "Willowbrook", "Birchfield", "Hawthorne"
]

# Fantasy club name suffixes
CLUB_SUFFIXES = [
    "United", "City", "Rangers", "Athletic", "Wanderers",
    "Town", "Rovers", "FC", "Hotspur", "Albion", "County",
    "Hearts", "Celtic", "Dynamos", "Strikers", "Titans", "Warriors"
]

# Random seed for reproducibility
RANDOM_SEED = None