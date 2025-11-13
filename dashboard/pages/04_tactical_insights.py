import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Tactical Insights", page_icon="⚔️", layout="wide")

LIVERPOOL_RED = "#C8102E"

@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).parent.parent.parent
    return pd.read_csv(BASE_DIR / 'data' / 'raw' / 'matches_2024_25.csv')

st.title("⚔️ Tactical Insights")
st.markdown("### Klopp's gegenpressing > Ten Hag's 'trust the process'")

with st.sidebar:
    st.error("🤡 United's tactics: Hope for individual brilliance. Liverpool's: Systematic excellence.")

matches = load_data()

st.markdown("---")
st.markdown("### 📊 Match Statistics Overview")

col1, col2, col3 = st.columns(3)

total_goals = matches['home_goals'].sum() + matches['away_goals'].sum()
avg_goals = total_goals / len(matches)
home_wins = (matches['home_goals'] > matches['away_goals']).sum()
home_win_pct = (home_wins / len(matches)) * 100

with col1:
    st.metric("📈 Avg Goals/Match", f"{avg_goals:.2f}")
with col2:
    st.metric("🏠 Home Win Rate", f"{home_win_pct:.1f}%")
with col3:
    st.metric("⚽ Total Goals", total_goals)

st.markdown("---")
st.markdown("### 🏠 Home vs Away Performance")

col1, col2 = st.columns(2)

with col1:
    home_wins = (matches['home_goals'] > matches['away_goals']).sum()
    home_draws = (matches['home_goals'] == matches['away_goals']).sum()
    home_losses = (matches['home_goals'] < matches['away_goals']).sum()
    
    home_stats = pd.DataFrame({
        'Result': ['Wins', 'Draws', 'Losses'],
        'Count': [home_wins, home_draws, home_losses]
    })
    
    fig = px.bar(home_stats, x='Result', y='Count', title='Home Team Results',
                color='Result', color_discrete_map={'Wins': LIVERPOOL_RED})
    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    away_wins = (matches['away_goals'] > matches['home_goals']).sum()
    away_draws = (matches['away_goals'] == matches['home_goals']).sum()
    away_losses = (matches['away_goals'] < matches['home_goals']).sum()
    
    away_stats = pd.DataFrame({
        'Result': ['Wins', 'Draws', 'Losses'],
        'Count': [away_wins, away_draws, away_losses]
    })
    
    fig2 = px.bar(away_stats, x='Result', y='Count', title='Away Team Results',
                 color='Result', color_discrete_map={'Wins': '#00B2A9'})
    st.plotly_chart(fig2, use_container_width=True)

st.error("🤡 **United's Tactical Philosophy:** Individual talent will save us (Narrator: It didn't)")
st.info("🔴 **Liverpool's Tactical Philosophy:** System > Stars. Gegenpressing + Data = Trophies")