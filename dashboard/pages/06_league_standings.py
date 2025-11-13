import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="League Standings", page_icon="📊", layout="wide")

LIVERPOOL_RED = "#C8102E"

@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).parent.parent.parent
    league = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'league_table_2024_25.csv')
    matches = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'matches_2024_25.csv')
    return league, matches

st.title("📊 League Standings & Match Results")
st.markdown("### Where Liverpool dominates and United... doesn't")

with st.sidebar:
    st.error("🏆 Liverpool: Champions League winners. United: Europa League strugglers.")

league_table, matches = load_data()

st.markdown("---")
st.markdown("### 🏆 Premier League Table 2024/25")

if not league_table.empty:
    league_display = league_table.sort_values('position').copy()
    
    st.dataframe(
        league_display[['position', 'club_name', 'played', 'won', 'drawn', 'lost', 
                       'goals_for', 'goals_against', 'goal_difference', 'points']],
        use_container_width=True,
        height=600
    )
    
    st.caption("🟢 Top 4 = Champions League | 🟡 5th = Europa League | 🔴 Bottom 3 = Relegation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        leader = league_table.iloc[0]
        st.metric("👑 League Leader", leader['club_name'], f"{leader['points']} pts")
    
    with col2:
        top_scorer_team = league_table.loc[league_table['goals_for'].idxmax()]
        st.metric("⚽ Top Scoring Team", top_scorer_team['club_name'], f"{top_scorer_team['goals_for']} goals")
    
    with col3:
        best_defense = league_table.loc[league_table['goals_against'].idxmin()]
        st.metric("🛡️ Best Defense", best_defense['club_name'], f"{best_defense['goals_against']} conceded")
    
    with col4:
        best_gd = league_table.loc[league_table['goal_difference'].idxmax()]
        st.metric("📊 Best Goal Diff", best_gd['club_name'], f"+{best_gd['goal_difference']}")

st.markdown("---")
st.markdown("### ⚽ Recent Match Results")

if not matches.empty:
    recent_matches = matches.tail(10)
    
    for _, match in recent_matches.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
        
        with col1:
            st.markdown(f"**{match['home_club_name']}**")
        with col2:
            st.markdown(f"<div style='text-align:center;font-size:20px;font-weight:bold'>{match['home_goals']}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='text-align:center'>-</div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div style='text-align:center;font-size:20px;font-weight:bold'>{match['away_goals']}</div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"**{match['away_club_name']}**")

st.error("🤡 **United's Season:** Start with hype, end with disappointment. Every. Year.")
st.success("🔴 **Liverpool's Season:** Consistent excellence through data-driven squad building.")