"""
Football Data Lab - Interactive Dashboard
Author: Abdullah Hasan Dafa
Email: dafa.abdullahhasan@gmail.com
Repository: https://github.com/hasandafa/football-data-lab

A Liverpool-biased, data-driven football analytics dashboard.
Pay your Sport Scientists or finish 8th like United.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import random
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Page configuration
st.set_page_config(
    page_title="Football Data Lab",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Liverpool colors
LIVERPOOL_RED = "#C8102E"
LIVERPOOL_GOLD = "#F6EB61"
LIVERPOOL_TEAL = "#00B2A9"

# Custom CSS
st.markdown(f"""
<style>
    .main {{background-color: #f8f9fa;}}
    .stButton>button {{
        background-color: {LIVERPOOL_RED};
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #a00d25;
        box-shadow: 0 4px 8px rgba(200, 16, 46, 0.3);
    }}
    h1, h2, h3 {{color: {LIVERPOOL_RED};}}
    [data-testid="stMetricValue"] {{color: {LIVERPOOL_RED}; font-weight: bold;}}
    
    /* Sidebar - Fix white background */
    [data-testid="stSidebar"] {{
        background-color: #262730 !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background-color: #262730 !important;
    }}
    
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: {LIVERPOOL_RED};
        color: white;
        text-align: center;
        padding: 10px;
        font-weight: bold;
        z-index: 999;
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all datasets from data/raw directory"""
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data' / 'raw'
    
    try:
        players = pd.read_csv(DATA_DIR / 'players.csv')
        clubs = pd.read_csv(DATA_DIR / 'clubs.csv')
        matches = pd.read_csv(DATA_DIR / 'matches_2024_25.csv')
        youth = pd.read_csv(DATA_DIR / 'youth_academy.csv')
        league_table = pd.read_csv(DATA_DIR / 'league_table_2024_25.csv')
        
        return players, clubs, matches, youth, league_table
    except FileNotFoundError as e:
        st.error(f"⚠️ Data files not found: {e}")
        st.info("Please ensure CSV files are in the data/raw/ directory")
        return None, None, None, None, None

# United roasts for sidebar
UNITED_ROASTS = [
    "🤡 £80M Maguire vs £8M Robertson. Pay your Sport Scientists!",
    "💸 £1B+ spent, 8th place. Try hiring Sport Scientists?",
    "🏆 Liverpool: 6 CLs. United: Living in the past since 2013.",
    "📊 Klopp's net spend < United's. Trophies > United's. Data wins.",
    "🧪 United's transfer strategy: Vibes > Science. Results: 8th place.",
    "💰 Pogba £89M vs Trent £0. One became world class. Guess which.",
    "🔴 Liverpool scouts with laptops > United scouts with dartboards.",
    "📈 Ten Hag: 'Trust the process'. The process: Europa League.",
    "🎯 United's recruitment: Hope > Analysis. Liverpool's: Science > Luck.",
    "⚽ Mount £55M, Casemiro £70M. Combined age: Ancient. Combined value: ?",
    "🏅 Liverpool's medals since 2018 > United's since 2013. Sport Scientists FTW!",
    "💡 Want to finish 8th? Copy United. Want trophies? Hire Sport Scientists."
]

def show_sidebar():
    """Display sidebar with navigation and United roasting"""
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background-color: {LIVERPOOL_RED}; 
                    border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0;'>⚽ Football Data Lab</h2>
            <p style='color: {LIVERPOOL_GOLD}; margin: 5px 0 0 0; font-size: 14px;'>
                Where Science Meets Football
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Navigation")
        st.info("Use the pages in the sidebar to explore different analyses!")
        
        # Random United roast
        st.error(random.choice(UNITED_ROASTS))
        
        st.markdown("---")
        st.markdown("### 💡 The Liverpool Way")
        st.success("**Data + Sport Scientists = Success**\n\nNot rocket science. Just ask Klopp.")
        
        st.markdown("---")
        st.markdown(f"""
        <div style='text-align: center; color: {LIVERPOOL_RED};'>
            <p style='font-size: 12px; margin: 0;'>
                Created by Abdullah Hasan Dafa<br>
                Liverpool Fan & Data Enthusiast
            </p>
        </div>
        """, unsafe_allow_html=True)

# Load data
players, clubs, matches, youth, league_table = load_data()

# Show sidebar
show_sidebar()

# Main content
if players is None:
    st.title("🚨 Data Not Found")
    st.error("Please load the data files first!")
    st.info("""
    **Required files in `data/raw/` directory:**
    - players.csv
    - clubs.csv
    - matches_2024_25.csv
    - youth_academy.csv
    - league_table_2024_25.csv
    """)
    st.stop()

# HOME PAGE
st.markdown(f"""
<div style='text-align: center; padding: 40px 20px; 
            background: linear-gradient(135deg, {LIVERPOOL_RED} 0%, #8B0A1F 100%); 
            border-radius: 15px; margin-bottom: 30px;'>
    <h1 style='color: white; font-size: 48px; margin: 0;'>⚽ Football Data Lab</h1>
    <p style='color: {LIVERPOOL_GOLD}; font-size: 24px; margin: 10px 0;'>
        Where Liverpool's Success Meets Data Science
    </p>
    <p style='color: white; font-size: 16px; margin: 10px 0;'>
        A Liverpool-biased, data-driven approach to football analytics
    </p>
</div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown("""
### 🎉 Welcome to the Football Data Lab!

This interactive dashboard showcases the power of **data-driven football analytics** with a heavy 
Liverpool FC bias (because we're 6-time European Champions and we actually use Sport Scientists).

Built with synthetic data representing the beautiful game, this project demonstrates how proper analytics 
and Sport Science can lead to success. Unlike some clubs who spent £1B+ only to finish 8th.

**Key Message:** Pay your Sport Scientists or finish 8th like United. Your choice. ⚽
""")

# Project stats overview
st.markdown("---")
st.markdown("### 📊 Project Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Total Players",
        value=f"{len(players):,}",
        delta="Elite Database"
    )

with col2:
    st.metric(
        label="🏟️ Clubs",
        value=len(clubs),
        delta="Premier League"
    )

with col3:
    st.metric(
        label="⚽ Matches Played",
        value=len(matches),
        delta="2024/25 Season"
    )

with col4:
    st.metric(
        label="🌟 Youth Players",
        value=len(youth),
        delta="Future Stars"
    )

st.markdown("---")

# Quick insights
col1, col2, col3 = st.columns(3)

with col1:
    top_player = players.loc[players['overall_rating'].idxmax()]
    # Get club name
    club_name = clubs[clubs['club_id'] == top_player['club_id']]['short_name'].values[0] if not clubs[clubs['club_id'] == top_player['club_id']].empty else 'Unknown'
    
    st.markdown(f"""
    <div style='background:white;padding:20px;border-radius:10px;border-left:4px solid {LIVERPOOL_RED}'>
        <h3 style='color:{LIVERPOOL_RED}'>🎯 Top Rated Player</h3>
        <p style='color:#333'><strong>{top_player['full_name']}</strong></p>
        <p style='color:#333'>Rating: <span style='color:{LIVERPOOL_RED};font-weight:bold'>{top_player['overall_rating']}/100</span></p>
        <p style='color:#333'>Club: {club_name}</p>
        <p style='color:#333'>Market Value: £{top_player['market_value']:.1f}M</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_goals = matches['home_goals'].sum() + matches['away_goals'].sum()
    avg_goals = total_goals / len(matches)
    home_wins = (matches['home_goals'] > matches['away_goals']).sum()
    home_win_pct = (home_wins / len(matches)) * 100
    
    st.markdown(f"""
    <div style='background:white;padding:20px;border-radius:10px;border-left:4px solid {LIVERPOOL_GOLD}'>
        <h3 style='color:{LIVERPOOL_RED}'>📈 Match Statistics</h3>
        <p style='color:#333'><strong>Avg Goals/Match:</strong> <span style='color:{LIVERPOOL_RED}'>{avg_goals:.2f}</span></p>
        <p style='color:#333'><strong>Home Win Rate:</strong> <span style='color:{LIVERPOOL_RED}'>{home_win_pct:.1f}%</span></p>
        <p style='color:#333'><strong>Total Goals:</strong> {total_goals}</p>
        <p style='color:#666;font-size:12px'>Exciting football action!</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    most_expensive = players.loc[players['market_value'].idxmax()]
    club_name_exp = clubs[clubs['club_id'] == most_expensive['club_id']]['short_name'].values[0] if not clubs[clubs['club_id'] == most_expensive['club_id']].empty else 'Unknown'
    
    st.markdown(f"""
    <div style='background:white;padding:20px;border-radius:10px;border-left:4px solid {LIVERPOOL_TEAL}'>
        <h3 style='color:{LIVERPOOL_RED}'>💰 Most Expensive Player</h3>
        <p style='color:#333'><strong>{most_expensive['full_name']}</strong></p>
        <p style='color:#333'>Value: <span style='color:{LIVERPOOL_RED}'>£{most_expensive['market_value']:.1f}M</span></p>
        <p style='color:#333'>Rating: {most_expensive['overall_rating']}/100</p>
        <p style='color:#333'>Club: {club_name_exp}</p>
    </div>
    """, unsafe_allow_html=True)

# League standings preview
st.markdown("---")
st.markdown("### 🏆 League Standings (Top 5)")

if league_table is not None and not league_table.empty:
    top_5 = league_table.head(5).copy()
    top_5.index = range(1, 6)
    
    st.dataframe(
        top_5[['club_name', 'played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'goal_difference', 'points']],
        use_container_width=True,
        height=220
    )
else:
    st.info("League standings will be displayed here once available.")

# United comparison
st.markdown("---")
st.markdown("### 🤡 United Reality Check")

col1, col2 = st.columns([2, 1])

with col1:
    st.error("""
    **Manchester United Transfer Efficiency:**
    - Money Spent: £1B+ (since 2013)
    - Premier League Titles: 0
    - Final Position 2023/24: 8th
    - Champions League: Europa League
    
    **Liverpool Transfer Efficiency:**
    - Smart recruitment with Sport Scientists
    - Multiple trophies with lower net spend
    - Consistent top 4 finishes
    - 2019 Champions League Winners
    
    **Lesson:** Pay your Sport Scientists or finish 8th.
    """)

with col2:
    # Placeholder for Liverpool badge
    st.markdown(f"""
    <div style='text-align:center;padding:40px;background:{LIVERPOOL_RED};border-radius:10px'>
        <h1 style='color:white;font-size:60px;margin:0'>LFC</h1>
        <p style='color:{LIVERPOOL_GOLD};margin:10px 0'>6x European Champions</p>
    </div>
    """, unsafe_allow_html=True)

# Value Score Analysis
st.markdown("---")
st.markdown("### 💎 Best Value Players (Value Score = Rating / Market Value × 10)")

# Calculate value scores
players['Value_Score'] = (players['overall_rating'] / players['market_value']) * 10

top_value_players = players.nlargest(10, 'Value_Score')[
    ['full_name', 'primary_position', 'overall_rating', 'market_value', 'Value_Score']
].copy()

# Get club names
top_value_players['club'] = top_value_players.apply(
    lambda row: clubs[clubs['club_id'] == players[players['full_name'] == row['full_name']]['club_id'].values[0]]['short_name'].values[0] 
    if len(players[players['full_name'] == row['full_name']]) > 0 else 'Unknown',
    axis=1
)

top_value_players = top_value_players[['full_name', 'club', 'primary_position', 'overall_rating', 'market_value', 'Value_Score']]
top_value_players.columns = ['Name', 'Club', 'Position', 'Rating', 'Market Value (£M)', 'Value Score']
top_value_players = top_value_players.reset_index(drop=True)
top_value_players.index = range(1, 11)

st.dataframe(
    top_value_players.style.format({
        'Market Value (£M)': '£{:.1f}M',
        'Value Score': '{:.2f}'
    }),
    use_container_width=True
)

st.success("💡 **Liverpool Strategy:** Target players with Value Score > 15 for maximum ROI!")

# Instructions
st.markdown("---")
st.markdown("### 🚀 How to Use This Dashboard")

st.info("""
**Navigate using the pages in the sidebar:**

1. **🔍 Player Explorer** - Search and filter players, view detailed stats and radar charts
2. **💰 Transfer Market** - Analyze player values, find bargains, avoid disasters
3. **🌟 Youth Academy** - Scout the next generation of talent
4. **⚔️ Tactical Insights** - Formations, playing styles, and match analysis
5. **🤖 Predictive Models** - ML-powered predictions for transfers and player development
6. **📊 League Standings** - Full league tables, match results, and head-to-head stats
7. **📖 About** - Project documentation and methodology

**Pro Tip:** Every page has at least one United roast. It's the Liverpool way. 🔴
""")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div class='footer'>
    YNWA - You'll Never Walk Alone | Football Data Lab by Abdullah Hasan Dafa | 
    <span style='background:{LIVERPOOL_GOLD};color:{LIVERPOOL_RED};padding:2px 8px;border-radius:3px;font-weight:bold'>
        Pay Your Sport Scientists
    </span>
</div>
""", unsafe_allow_html=True)