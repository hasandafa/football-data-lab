import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Transfer Market", page_icon="💰", layout="wide")

LIVERPOOL_RED = "#C8102E"
LIVERPOOL_GOLD = "#F6EB61"
LIVERPOOL_TEAL = "#00B2A9"

@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).parent.parent.parent
    players = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'players.csv')
    clubs = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'clubs.csv')
    players = players.merge(clubs[['club_id', 'short_name']], on='club_id', how='left')
    return players

st.title("💰 Transfer Market Analysis")
st.markdown("### Find Liverpool-style bargains, avoid United-style disasters")

with st.sidebar:
    st.error("💸 United's £1B budget → 8th place. Liverpool's data → Trophies.")

players = load_data()
players['Value_Score'] = (players['overall_rating'] / players['market_value']) * 10

st.markdown("---")
st.markdown("### 📊 Market Value vs Rating Analysis")

fig = px.scatter(
    players,
    x='market_value',
    y='overall_rating',
    color='age',
    size='Value_Score',
    hover_data=['full_name', 'primary_position', 'short_name', 'Value_Score'],
    title='Transfer Market: Value vs Quality',
    labels={'market_value': 'Market Value (£M)', 'overall_rating': 'Player Rating'},
    color_continuous_scale='RdYlGn_r',
    height=600
)

fig.add_shape(
    type="rect", x0=0, y0=80, x1=50, y1=100,
    fillcolor=LIVERPOOL_RED, opacity=0.2, layer="below", line_width=0,
)
fig.add_annotation(x=25, y=90, text="🔴 Liverpool Zone<br>(Good Value)", showarrow=False)

fig.add_shape(
    type="rect", x0=70, y0=60, x1=200, y1=80,
    fillcolor="gray", opacity=0.2, layer="below", line_width=0,
)
fig.add_annotation(x=135, y=70, text="🤡 United Zone<br>(Overpaid)", showarrow=False)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 🏆 Top 20 Best Value Players")

top_value = players.nlargest(20, 'Value_Score')[
    ['full_name', 'age', 'primary_position', 'short_name', 'overall_rating', 'market_value', 'Value_Score']
].reset_index(drop=True)
top_value.columns = ['Name', 'Age', 'Position', 'Club', 'Rating', 'Market Value (£M)', 'Value Score']
top_value.index = range(1, 21)

st.dataframe(
    top_value.style.format({
        'Market Value (£M)': '£{:.1f}M',
        'Value Score': '{:.2f}'
    }),
    use_container_width=True,
    height=400
)

st.success("💡 **Liverpool Strategy:** Target players with Value Score > 15 for maximum ROI!")

st.markdown("---")
st.error("""
🤡 **United's Transfer Disasters:**

Total waste on 5 players: £360M+
- Maguire £80M (worth £30M)
- Antony £85M (worth £40M)  
- Sancho £73M (worth £45M)
- Mount £55M (worth £25M)
- Casemiro £70M at age 30 (declining)

**With that money, Liverpool bought:**
Salah (£37M), Van Dijk (£75M), Alisson (£65M), Fabinho (£40M) = Multiple trophies

**Lesson:** Hire Sport Scientists. Use data. Don't rely on vibes.
""")

st.info("💡 **The Liverpool Method:** Rating > 80, Age 23-27, Value Score > 12 = Smart transfer!")