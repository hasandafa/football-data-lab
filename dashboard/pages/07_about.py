import streamlit as st

st.set_page_config(page_title="About", page_icon="📖", layout="wide")

LIVERPOOL_RED = "#C8102E"
LIVERPOOL_GOLD = "#F6EB61"

st.title("📖 About Football Data Lab")
st.markdown("### The story behind Liverpool's data-driven success")

with st.sidebar:
    st.error("🎓 Education: Liverpool's Sport Scientists > United's Social Media Team")

st.markdown("---")
st.markdown("## 🏆 Project Motivation")

st.markdown(f"""
<div style='background:white;padding:30px;border-radius:10px;border-left:5px solid {LIVERPOOL_RED}'>
    <p style='font-size:16px'>
        This project was born from a simple observation: <strong>Jürgen Klopp's Liverpool dominated 
        modern football not through unlimited spending, but through intelligent use of data and Sport Science.</strong>
    </p>
    
    <p>While clubs like Manchester United threw £1B+ at the transfer market:</p>
    <ul>
        <li>✅ Liverpool signed Mohamed Salah for £37M (now worth £150M+)</li>
        <li>✅ Developed Trent Alexander-Arnold from academy (£0 cost, priceless value)</li>
        <li>✅ Used data to identify undervalued talents (Robertson £8M, Wijnaldum £25M)</li>
        <li>✅ Won the Premier League, Champions League, and multiple cups</li>
    </ul>
    
    <p style='font-size:18px;font-weight:bold;color:{LIVERPOOL_RED}'>
        The lesson is clear: Pay your Sport Scientists, or finish 8th like United.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 📊 Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style='background:{LIVERPOOL_RED};color:white;padding:20px;border-radius:10px'>
        <h3 style='color:white'>Dataset Statistics</h3>
        <ul>
            <li><strong>479 Players</strong> with detailed attributes</li>
            <li><strong>20 Clubs</strong> in simulation</li>
            <li><strong>380 Matches</strong> from 2024/25 season</li>
            <li><strong>100 Youth Players</strong> with growth potential</li>
        </ul>
        <p>All synthetically generated to demonstrate football analytics principles.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background:{LIVERPOOL_GOLD};color:#333;padding:20px;border-radius:10px'>
        <h3>Key Features</h3>
        <ul>
            <li>Realistic player ratings (40-99)</li>
            <li>Position-specific attributes</li>
            <li>Market value calculations</li>
            <li>Youth development trajectories</li>
            <li>Match results with formations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 🛠️ Technology Stack")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.info("""
    **Data & Analysis**
    - Python 3.10+
    - Pandas
    - NumPy
    - Scikit-learn
    """)

with tech_col2:
    st.info("""
    **Visualization**
    - Streamlit
    - Plotly
    - Matplotlib
    - Seaborn
    """)

with tech_col3:
    st.info("""
    **Development**
    - Git & GitHub
    - Jupyter Notebooks
    - VS Code
    """)

st.markdown("---")
st.markdown("## 💡 Key Insights")

insights = [
    ("🎯 Value Investing Works", "Players with high Rating/Value ratios outperform expensive signings."),
    ("🌟 Youth Development ROI", "Academy products offer 200%+ ROI vs equivalent transfers."),
    ("📊 Age Sweet Spot", "Players aged 24-27 offer best performance + value combination."),
    ("🔬 Sport Science Matters", "Data-driven training extends careers by 2-3 years."),
    ("⚔️ System > Stars", "Tactical cohesion matters more than individual talent.")
]

for title, content in insights:
    st.markdown(f"""
    <div style='background:#f8f9fa;padding:15px;border-radius:10px;margin:10px 0;border-left:4px solid {LIVERPOOL_RED}'>
        <h4 style='color:{LIVERPOOL_RED};margin-top:0'>{title}</h4>
        <p style='margin:0'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 👨‍💻 About the Author")

st.markdown(f"""
<div style='background:{LIVERPOOL_RED};color:white;padding:30px;border-radius:10px;text-align:center'>
    <h2 style='color:white'>Abdullah Hasan Dafa</h2>
    <p style='font-size:18px;color:{LIVERPOOL_GOLD}'>Data Enthusiast & Liverpool FC Supporter</p>
    <p>📧 Email: dafa.abdullahhasan@gmail.com</p>
    <p>🔗 GitHub: <a href='https://github.com/hasandafa/football-data-lab' 
       style='color:{LIVERPOOL_GOLD}'>github.com/hasandafa/football-data-lab</a></p>
    <p>📝 Article: Substack (coming soon)</p>
    <p style='margin-top:20px'>
        Built with passion for football analytics and a healthy dose of United mockery. 🔴⚽
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
<div style='background:linear-gradient(135deg, {LIVERPOOL_RED} 0%, #8B0A1F 100%);
            color:white;padding:40px;border-radius:15px;text-align:center'>
    <h1 style='color:white;font-size:48px'>YNWA</h1>
    <h2 style='color:{LIVERPOOL_GOLD};font-size:32px'>You'll Never Walk Alone</h2>
    <p style='font-size:18px'>6 European Cups | 19 League Titles | Countless Memories</p>
    <p style='font-size:20px;font-weight:bold;color:{LIVERPOOL_GOLD};margin-top:30px'>
        This is Anfield. This is Liverpool. This is Data Science.
    </p>
</div>
""", unsafe_allow_html=True)

st.info("**Remember:** Pay your Sport Scientists. Always. 🔴⚽📊")
