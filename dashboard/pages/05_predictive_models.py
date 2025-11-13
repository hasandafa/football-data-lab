import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Predictive Models", page_icon="🤖", layout="wide")

LIVERPOOL_RED = "#C8102E"
LIVERPOOL_GOLD = "#F6EB61"

st.title("🤖 Predictive Models")
st.markdown("### Machine Learning: Liverpool's Secret Weapon")

with st.sidebar:
    st.error("🧮 Liverpool: Data-driven decisions. United: Gut feelings. Results speak.")

st.markdown("---")
st.markdown("### 📈 Player Rating Predictor")

st.info("**Predict how a player's rating will develop over their career**")

col1, col2, col3 = st.columns(3)

with col1:
    pred_age = st.slider("Current Age", 16, 35, 21)
with col2:
    pred_rating = st.slider("Current Rating", 40, 99, 70)
with col3:
    pred_potential = st.slider("Potential", 40, 99, 85)

if st.button("🔮 Predict Career Trajectory", type="primary"):
    ages = [21, 23, 25, 27, 29]
    predictions = []
    
    for target_age in ages:
        if target_age <= pred_age:
            predicted = pred_rating
        else:
            years = target_age - pred_age
            growth = pred_potential - pred_rating
            
            if target_age <= 24:
                factor = 0.30
            elif target_age <= 27:
                factor = 0.20
            else:
                factor = 0.10
            
            total_growth = min(growth, growth * factor * years)
            predicted = min(pred_rating + total_growth, pred_potential)
        
        predictions.append(round(predicted, 1))
    
    traj_df = pd.DataFrame({'Age': ages, 'Predicted Rating': predictions})
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=traj_df['Age'], y=traj_df['Predicted Rating'],
        mode='lines+markers', name='Predicted Rating',
        line=dict(color=LIVERPOOL_RED, width=3), marker=dict(size=10)
    ))
    
    fig.add_hline(y=pred_potential, line_dash="dash", line_color=LIVERPOOL_GOLD,
                  annotation_text=f"Max Potential: {pred_potential}")
    
    fig.update_layout(title="Career Rating Trajectory", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📊 Predicted Ratings")
    pred_col1, pred_col2, pred_col3, pred_col4 = st.columns(4)
    pred_col1.metric("At Age 21", f"{predictions[0]}/100")
    pred_col2.metric("At Age 23", f"{predictions[1]}/100")
    pred_col3.metric("At Age 25", f"{predictions[2]}/100")
    pred_col4.metric("At Age 27 (Peak)", f"{predictions[3]}/100")

st.markdown("---")
st.error("🤡 **United's Model:** Instagram followers = Good signing. **Result:** 8th place")
st.success("🔴 **Liverpool's Model:** Rating + Age + Value + System fit = Trophies")
