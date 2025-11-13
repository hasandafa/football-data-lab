import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Youth Academy", page_icon="🌟", layout="wide")

LIVERPOOL_RED = "#C8102E"
LIVERPOOL_GOLD = "#F6EB61"

@st.cache_data
def load_youth():
    BASE_DIR = Path(__file__).parent.parent.parent
    return pd.read_csv(BASE_DIR / 'data' / 'raw' / 'youth_academy.csv')

st.title("🌟 Youth Academy")
st.markdown("### Develop the next Trent Alexander-Arnold (£0 academy product)")

with st.sidebar:
    st.error("💰 Liverpool's £0 Trent > United's £89M Pogba. Academy >>> Overpaying!")

youth = load_youth()

st.markdown("---")
st.markdown("### 🎯 Elite Youth Prospects (Potential 80+)")

elite_youth = youth[youth['potential'] >= 80].copy()

if not elite_youth.empty:
    elite_youth['Growth_Potential'] = elite_youth['potential'] - elite_youth['overall_rating']
    
    def assess_readiness(row):
        if row['overall_rating'] >= 70:
            return '🟢 Ready'
        elif row['overall_rating'] >= 65:
            return '🟡 Almost'
        else:
            return '🔴 Developing'
    
    elite_youth['Readiness'] = elite_youth.apply(assess_readiness, axis=1)
    
    display_df = elite_youth[['full_name', 'age', 'primary_position', 'overall_rating', 
                               'potential', 'Growth_Potential', 'Readiness']].copy()
    display_df.columns = ['Name', 'Age', 'Position', 'Current Rating', 'Potential', 
                          'Growth Potential', 'Readiness']
    
    st.dataframe(
        display_df.sort_values('Potential', ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=400
    )
    
    st.success(f"🌟 Found {len(elite_youth)} elite prospects with potential 80+!")
else:
    st.warning("No youth players with potential 80+ found.")

st.markdown("---")
st.markdown("### 💰 Academy ROI Calculator")

col1, col2, col3 = st.columns(3)

with col1:
    num_promoted = st.number_input("Youth players promoted", 0, 20, 5)
with col2:
    avg_value = st.number_input("Avg market value if sold (£M)", 0, 100, 30)
with col3:
    academy_cost = st.number_input("Total academy cost (£M/year)", 0, 50, 5)

total_value = num_promoted * avg_value
roi = ((total_value - academy_cost) / academy_cost * 100) if academy_cost > 0 else 0

result_col1, result_col2, result_col3 = st.columns(3)

with result_col1:
    st.metric("💰 Total Value Generated", f"£{total_value:.0f}M")
with result_col2:
    st.metric("📊 Net Profit", f"£{total_value - academy_cost:.0f}M")
with result_col3:
    st.metric("📈 ROI", f"{roi:.0f}%")

if roi > 200:
    st.success("🟢 **Outstanding ROI!** This is the Liverpool way!")
elif roi > 100:
    st.info("🟡 **Good ROI** - Academy is paying off nicely.")
else:
    st.warning("🔴 **Low ROI** - Need to improve youth development system.")

st.markdown("---")
comparison_df = pd.DataFrame({
    'Metric': ['Transfer Fee', 'Academy Product', 'Peak Rating', 'Trophies', 'Club Legend', 'Value to Club'],
    'Trent (Liverpool)': ['£0', '✅ Yes', '89', 'PL, CL, FA, EFL', '✅ Legend', 'Priceless'],
    'Pogba (United)': ['£89M', '❌ No', '86', '0 PL, 0 CL', '❌ Left free', '£0']
})

st.markdown("### 🔴 Liverpool's £0 Trent vs 🤡 United's £89M Pogba")
st.table(comparison_df.set_index('Metric'))

st.error("**Moral:** Invest in your academy. Invest in Sport Scientists. Don't be like United.")