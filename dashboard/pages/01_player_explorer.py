import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Player Explorer", page_icon="🔍", layout="wide")

LIVERPOOL_RED = "#C8102E"
LIVERPOOL_GOLD = "#F6EB61"
LIVERPOOL_TEAL = "#00B2A9"

st.markdown(f"""
<style>
    .stButton>button {{background-color: {LIVERPOOL_RED}; color: white;}}
    h1, h2, h3 {{color: {LIVERPOOL_RED};}}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).parent.parent.parent
    players = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'players.csv')
    clubs = pd.read_csv(BASE_DIR / 'data' / 'raw' / 'clubs.csv')
    return players, clubs

st.title("🔍 Player Explorer")
st.markdown("### Find the next Mo Salah (£37M gem) or avoid the next Maguire (£80M disaster)")

with st.sidebar:
    st.error("🤡 £80M Maguire rating < £37M Salah rating. Pay your Sport Scientists!")

players, clubs = load_data()

# Merge club names
players = players.merge(clubs[['club_id', 'short_name']], on='club_id', how='left')

st.markdown("---")
st.markdown("### 🎯 Filter Players")

col1, col2, col3, col4 = st.columns(4)

with col1:
    positions = ['All'] + sorted(players['primary_position'].unique().tolist())
    position_filter = st.selectbox("Position", positions)

with col2:
    age_range = st.slider("Age Range", int(players['age'].min()), 
                          int(players['age'].max()), (18, 35))

with col3:
    nationalities = ['All'] + sorted(players['nationality'].unique().tolist())
    nationality_filter = st.selectbox("Nationality", nationalities)

with col4:
    clubs_list = ['All'] + sorted(players['short_name'].dropna().unique().tolist())
    club_filter = st.selectbox("Club", clubs_list)

col1, col2, col3 = st.columns(3)

with col1:
    rating_range = st.slider("Overall Rating", 40, 99, (60, 99))

with col2:
    search_name = st.text_input("🔎 Search Player Name")

with col3:
    indonesian_only = st.checkbox("🇮🇩 Indonesian Players Only")

# Apply filters
filtered = players.copy()

if position_filter != 'All':
    filtered = filtered[filtered['primary_position'] == position_filter]
    
filtered = filtered[(filtered['age'] >= age_range[0]) & (filtered['age'] <= age_range[1])]

if nationality_filter != 'All':
    filtered = filtered[filtered['nationality'] == nationality_filter]
    
if club_filter != 'All':
    filtered = filtered[filtered['short_name'] == club_filter]
    
filtered = filtered[(filtered['overall_rating'] >= rating_range[0]) & 
                   (filtered['overall_rating'] <= rating_range[1])]

if search_name:
    filtered = filtered[filtered['full_name'].str.contains(search_name, case=False, na=False)]
    
if indonesian_only:
    filtered = filtered[filtered['nationality'] == 'Indonesia']

st.markdown(f"### 📊 Found {len(filtered)} Players")

# Sort options
col1, col2 = st.columns([3, 1])
with col2:
    sort_by = st.selectbox("Sort by", ['overall_rating', 'age', 'market_value', 
                                        'potential', 'full_name'])
    sort_order = st.radio("Order", ['Descending', 'Ascending'], horizontal=True)
    
filtered_sorted = filtered.sort_values(by=sort_by, 
                                       ascending=(sort_order == 'Ascending'))

# Display table
display_cols = ['full_name', 'age', 'primary_position', 'short_name', 'nationality', 
                'overall_rating', 'potential', 'market_value']

if not filtered_sorted.empty:
    display_df = filtered_sorted[display_cols].copy()
    display_df.columns = ['Name', 'Age', 'Position', 'Club', 'Nationality', 
                          'Rating', 'Potential', 'Market Value (£M)']
    
    st.dataframe(
        display_df.reset_index(drop=True).style.format({
            'Market Value (£M)': '£{:.1f}M'
        }),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="filtered_players.csv",
        mime="text/csv"
    )
else:
    st.warning("No players found with current filters.")

# Player detail view
st.markdown("---")
st.markdown("### 👤 Player Detail View")

if not filtered_sorted.empty:
    player_names = filtered_sorted['full_name'].tolist()
    selected_player_name = st.selectbox("Select a player to view details", 
                                        ['Choose a player...'] + player_names)
    
    if selected_player_name != 'Choose a player...':
        player = filtered_sorted[filtered_sorted['full_name'] == selected_player_name].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div style='background:white;padding:20px;border-radius:10px;border-left:4px solid {LIVERPOOL_RED}'>
                <h2 style='color:{LIVERPOOL_RED};margin-top:0'>{player['full_name']}</h2>
                <p style='color:#333'><strong>Age:</strong> {player['age']}</p>
                <p style='color:#333'><strong>Position:</strong> {player['primary_position']}</p>
                <p style='color:#333'><strong>Club:</strong> {player['short_name']}</p>
                <p style='color:#333'><strong>Nationality:</strong> {player['nationality']}</p>
                <p style='color:#333'><strong>Rating:</strong> <span style='color:{LIVERPOOL_RED};font-size:24px;font-weight:bold'>{player['overall_rating']}</span>/100</p>
                <p style='color:#333'><strong>Potential:</strong> {player['potential']}/100</p>
                <p style='color:#333'><strong>Market Value:</strong> £{player['market_value']:.1f}M</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Value score
            value_score = (player['overall_rating'] / player['market_value']) * 10 if player['market_value'] > 0 else 0
            
            if value_score > 15:
                recommendation = "🟢 BUY - Excellent Value!"
                reason = "High rating relative to market value. Liverpool-style bargain."
            elif value_score > 10:
                recommendation = "🟡 CONSIDER - Fair Value"
                reason = "Decent value but not exceptional. Worth monitoring."
            else:
                recommendation = "🔴 AVOID - Overpriced"
                reason = "High price for the rating. United-style overpay."
            
            st.markdown(f"""
            <div style='background:white;padding:15px;border-radius:10px;margin-top:20px;border-left:4px solid {LIVERPOOL_GOLD}'>
                <h4 style='color:{LIVERPOOL_RED}'>💡 Transfer Recommendation</h4>
                <p style='font-size:18px;font-weight:bold;color:#333'>{recommendation}</p>
                <p style='color:#333'><strong>Value Score:</strong> {value_score:.2f}</p>
                <p style='color:#666;font-size:14px'>{reason}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Radar chart for attributes - Only show attributes with valid values
            all_attributes = {
                'Pace': 'phys_pace',
                'Shooting': 'tech_shooting', 
                'Passing': 'tech_passing',
                'Dribbling': 'tech_dribbling',
                'Tackling': 'tech_tackling',
                'Stamina': 'phys_stamina',
                'Strength': 'phys_strength',
                'Ball Control': 'tech_ball_control',
                'Vision': 'mental_vision',
                'Work Rate': 'mental_work_rate'
            }
            
            # Filter only attributes that exist and have valid values
            valid_attributes = {}
            for label, col in all_attributes.items():
                if col in player.index and pd.notna(player[col]) and player[col] > 0:
                    valid_attributes[label] = col
            
            if len(valid_attributes) >= 3:
                attr_labels = list(valid_attributes.keys())
                attributes = list(valid_attributes.values())
                values = [float(player[attr]) for attr in attributes]
                
                # Calculate position average for valid attributes only
                pos_players = filtered[filtered['primary_position'] == player['primary_position']]
                if len(pos_players) > 1:
                    avg_values = [float(pos_players[attr].mean()) for attr in attributes]
                else:
                    avg_values = values
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=attr_labels + [attr_labels[0]],
                    fill='toself',
                    name=player['full_name'],
                    line_color=LIVERPOOL_RED,
                    fillcolor=f'rgba(200, 16, 46, 0.3)'
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=avg_values + [avg_values[0]],
                    theta=attr_labels + [attr_labels[0]],
                    fill='toself',
                    name=f'{player["primary_position"]} Average',
                    line_color='#888888',
                    fillcolor='rgba(136, 136, 136, 0.2)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100])
                    ),
                    showlegend=True,
                    title=f"{player['full_name']} vs Position Average",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough attribute data to display radar chart")
            
            # Detailed stats
            st.markdown("#### 📊 Key Attributes")
            
            attr_col1, attr_col2, attr_col3 = st.columns(3)
            
            key_attrs = {
                'Pace': 'phys_pace',
                'Shooting': 'tech_shooting', 
                'Passing': 'tech_passing',
                'Dribbling': 'tech_dribbling',
                'Tackling': 'tech_tackling',
                'Stamina': 'phys_stamina',
                'Ball Control': 'tech_ball_control',
                'Vision': 'mental_vision',
                'Work Rate': 'mental_work_rate'
            }
            
            for i, (label, col) in enumerate(key_attrs.items()):
                if col in player.index and pd.notna(player[col]):
                    with [attr_col1, attr_col2, attr_col3][i % 3]:
                        st.metric(label, f"{int(player[col])}/100")
else:
    st.info("Apply filters to see players.")

st.markdown("---")
st.info("💡 **The Liverpool Way:** Sign players with high value scores. Leave the overpriced ones to United.")