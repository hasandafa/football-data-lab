"""
Staff generation module
Generate coaching and support staff for clubs
"""

import pandas as pd
from src.clubs import generate_club_staff


def generate_all_staff(clubs: pd.DataFrame) -> pd.DataFrame:
    """
    Generate staff for all clubs
    
    Args:
        clubs: DataFrame of all clubs
        
    Returns:
        DataFrame with all staff members
    """
    all_staff = []
    
    for _, club in clubs.iterrows():
        club_staff = generate_club_staff(club["club_id"], club["tier"])
        all_staff.append(club_staff)
    
    return pd.concat(all_staff, ignore_index=True)


if __name__ == "__main__":
    from src.clubs import generate_clubs
    
    print("Generating test clubs and staff...")
    clubs = generate_clubs(num_clubs=3)
    staff = generate_all_staff(clubs)
    print(f"\nGenerated staff for {len(clubs)} clubs")
    print(f"Total staff members: {len(staff)}")
    print(staff[["full_name", "club_id", "role", "nationality"]])