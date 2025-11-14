# ⚽ Football Data Lab

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Liverpool](https://img.shields.io/badge/Liverpool-6x_European_Champions-C8102E.svg)](https://www.liverpoolfc.com)
[![Liverpool](https://img.shields.io/badge/Liverpool-20x_League_Champions-C8102E.svg)](https://www.liverpoolfc.com)

**A Liverpool-biased, data-driven football analytics project demonstrating the power of Sport Science and intelligent recruitment.**

> *"Pay your Sport Scientists or finish 8th like United. Your choice."* ⚽🔴

---

## 🏆 Project Overview

Football Data Lab is a comprehensive data science project that analyzes football (soccer) data using:
- **Synthetic data generation** for realistic player attributes and match statistics
- **Exploratory data analysis** to uncover patterns and insights
- **Predictive modeling** for transfer decisions and player development
- **Interactive dashboard** for visualizing analytics in real-time

**Key Message:** This project demonstrates how Liverpool's data-driven approach with Sport Scientists leads to success, while United's £1B+ spending without proper analytics leads to 8th place finishes.

---

## 📊 Dataset

### Synthetic Data Generated:
- **479 Players** - Complete profiles with ratings, physical/technical/mental attributes
- **20 Clubs** - Premier League simulation with stadium and city data
- **380 Matches** - Full 2024/25 season with formations and playing styles
- **100 Youth Academy Players** - Prospects with growth potential
- **League Table** - Current standings with full statistics

All data is synthetically generated to maintain realistic distributions while demonstrating analytics principles.

---

## 🗂️ Project Structure

```
football-data-lab/
├── data/
│   ├── raw/                          # Original CSV data files
│   │   ├── clubs.csv
│   │   ├── league_info.csv
│   │   ├── league_table_2024_25.csv
│   │   ├── matches_2024_25.csv
│   │   ├── players.csv
│   │   ├── seasons.csv
│   │   ├── staff.csv
│   │   ├── transfer_history.csv
│   │   └── youth_academy.csv
│   └── processed/                    # Cleaned and processed data
│
├── notebooks/                        # Jupyter notebooks for analysis
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_player_value_analysis.ipynb
│   ├── 03_transfer_market_intelligence.ipynb
│   ├── 04_youth_academy_goldmine.ipynb
│   ├── 05_tactical_insights.ipynb
│   └── 06_predictive_modeling.ipynb
│
├── dashboard/                        # Streamlit dashboard
│   ├── app.py                        # Main application
│   └── pages/                        # Dashboard pages
│       ├── 01_player_explorer.py
│       ├── 02_transfer_market.py
│       ├── 03_youth_academy.py
│       ├── 04_tactical_insights.py
│       ├── 05_predictive_models.py
│       ├── 06_league_standings.py
│       └── 07_about.py
│
├── src/                              # Source code modules
│   ├── clubs.py
│   ├── config.py
│   ├── leagues.py
│   ├── matches.py
│   ├── players.py
│   ├── staff.py
│   ├── transfers.py
│   ├── utils.py
│   └── youth_academy.py
│
├── .gitignore
├── requirements.txt
└── README.md                         # This file
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/hasandafa/football-data-lab.git
cd football-data-lab
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Synthetic Data
**IMPORTANT:** Before exploring notebooks or running the dashboard, you need to generate the synthetic football data first!

```bash
python generate_data.py
```

This script will generate all required data files in `data/raw/`:
- ✅ **players.csv** - 479 players with complete attributes
- ✅ **clubs.csv** - 20 Premier League clubs  
- ✅ **matches_2024_25.csv** - 380 matches with results
- ✅ **youth_academy.csv** - 100 youth prospects
- ✅ **league_table_2024_25.csv** - Current standings
- ✅ **staff.csv** - Managers and coaching staff
- ✅ **seasons.csv** - Season information
- ✅ **transfer_history.csv** - Historical transfers
- ✅ **league_info.csv** - League configuration

**Generation time:** ~30-60 seconds  
**Data quality:** Realistic distributions using advanced algorithms in `src/` modules

### 4. Explore the Notebooks
```bash
jupyter notebook
```
Navigate to `notebooks/` and start with `01_exploratory_data_analysis.ipynb`

### 5. Run the Dashboard
```bash
cd dashboard
streamlit run app.py
```
Dashboard opens at `http://localhost:8501` 🎉

---

## 📁 Data Generation Architecture

The project uses a modular data generation system located in the `src/` directory:

### Core Modules (`src/`)

```
src/
├── config.py              # All configuration and constants
├── utils.py               # Helper functions (names, IDs, calculations)
├── leagues.py             # League and season structure
├── clubs.py               # Club generation with tiers
├── players.py             # Player generation with realistic attributes
├── staff.py               # Manager and coaching staff
├── youth_academy.py       # Youth prospects generation
├── matches.py             # Match fixtures and simulation
└── transfers.py           # Transfer history generation
```

### How Data Generation Works

1. **Configuration** (`config.py`)
   - Defines all parameters: league structure, squad sizes, age distributions
   - Sets attribute ranges by position (GK, DEF, MID, FWD)
   - Configures realistic market values and wages

2. **League & Clubs** (`leagues.py`, `clubs.py`)
   - Creates 20-team league with 3 tiers (top/mid/lower)
   - Generates club names, stadiums, budgets, reputations
   - Assigns playing styles and formations

3. **Players** (`players.py`)
   - Generates 23-30 players per club
   - Position-specific attributes (physical, technical, mental)
   - Age-based attribute adjustments
   - Realistic potential calculations
   - **Market values up to £200M** (realistic 2024/25 economics)

4. **Youth Academy** (`youth_academy.py`)
   - Creates 5 youth players (16-17 years) per club
   - Elite prospects with high potential (80+)
   - Promotion readiness assessment

5. **Matches** (`matches.py`)
   - Generates double round-robin fixtures (38 matches per team)
   - Simulates all 380 matches using team strength
   - Calculates league table with standings

6. **Staff & Transfers** (`staff.py`, `transfers.py`)
   - Generates managers and coaching staff
   - Creates historical transfer records

### Key Features of Generated Data

✅ **Realistic Distributions:**
- Player ages follow professional football patterns
- Attributes vary by position and age
- Market values reflect 2024/25 economics

✅ **Smart Calculations:**
- Overall ratings use position-weighted attributes
- Market values consider age, potential, and position
- Wages scale with player value

✅ **Quality Control:**
- Top-tier clubs get better players (rating adjustment)
- Nationality weights match global football demographics
- Indonesian players included (🇮🇩 representation!)

### Customizing Data Generation

Edit `src/config.py` to adjust:
- Number of teams, squad sizes
- Age distributions, attribute ranges  
- Market value calculations
- Nationalities and weights

Then re-run `python generate_data.py` to regenerate with new settings!

---

## 📓 Jupyter Notebooks

### 1. **Exploratory Data Analysis**
- Dataset overview and statistics
- Distribution analysis
- Correlation studies
- Initial insights

### 2. **Player Value Analysis**
- Value score calculations (Rating/Market Value)
- Age vs Value analysis
- Position-specific valuations
- Liverpool-style bargain identification

### 3. **Transfer Market Intelligence**
- Market trends analysis
- Overvalued vs Undervalued players
- Transfer success prediction
- Liverpool vs United comparison

### 4. **Youth Academy Goldmine**
- Elite prospects identification
- Growth trajectory modeling
- Promotion readiness assessment
- ROI calculations
- Trent Alexander-Arnold case study

### 5. **Tactical Insights**
- Formation effectiveness
- Playing style analysis
- Home advantage studies
- Match outcome prediction

### 6. **Predictive Modeling**
- Player rating predictions
- Transfer success classification
- Youth development forecasting
- Model evaluation and validation

---

## 🎨 Dashboard Features

### Interactive Streamlit Application with:

**🏠 Home Page**
- Project overview with Liverpool pride
- Quick statistics cards
- League standings preview
- United reality check

**🔍 Player Explorer**
- Advanced filtering and search
- Indonesian player spotlight
- Radar chart comparisons
- Transfer recommendations

**💰 Transfer Market Analysis**
- Value vs Rating scatter plots
- Best value players identification
- Transfer calculator
- United disaster analysis

**🌟 Youth Academy**
- Growth trajectory visualizations
- Promotion readiness system
- ROI calculator
- Academy success stories

**⚔️ Tactical Insights**
- Formation effectiveness
- Playing style distribution
- Head-to-head simulator

**🤖 Predictive Models**
- Career trajectory predictions
- Transfer success probability
- Youth development simulator

**📊 League Standings**
- Full league table
- Match results
- Team comparisons
- Leaderboards

---

## 🔬 Key Insights

### 1. **Value Investing Works**
Players with Value Score > 15 (Rating/Market Value × 10) consistently outperform expensive signings. Liverpool's approach validated.

### 2. **Youth Development ROI**
Academy products offer 200%+ ROI compared to equivalent transfers. Liverpool's Trent (£0) > United's Pogba (£89M).

### 3. **Age Sweet Spot**
Players aged 24-27 offer the best combination of performance and value. Avoid United's mistake of overpaying for 30+ year olds.

### 4. **Sport Science Matters**
Data-driven training extends player careers by 2-3 years on average. This is Liverpool's secret weapon.

### 5. **System > Stars**
Tactical cohesion matters more than individual talent. Liverpool's gegenpressing > United's vibes.

---

## 💡 The Liverpool Way

This project demonstrates Liverpool's successful framework:

1. **Data-Driven Recruitment**
   - Value score > 15 = Smart signing
   - Age 24-27 = Peak performance window
   - Rating/Value ratio is king

2. **Sport Science Investment**
   - Injury prevention through load management
   - Performance optimization
   - Career longevity

3. **Youth Development**
   - Patient development over quick fixes
   - Academy ROI > Transfer spending
   - Build club culture

4. **Tactical Consistency**
   - Clear playing philosophy
   - Sign players who fit the system
   - System > Individual brilliance

5. **Sustainable Finance**
   - Never overpay for transfers
   - Sell high on players past their peak
   - Reinvest profits intelligently

**Result:** 6 European Cups, consistent success, global admiration.

---

## 🤡 United's Cautionary Tale

What NOT to do (based on data):

- ❌ Panic buying (£80M Maguire, £85M Antony)
- ❌ Ignoring analytics and Sport Scientists
- ❌ Overpaying for aging players (Casemiro £70M at age 30)
- ❌ No tactical philosophy or consistency
- ❌ £1B+ spent since 2013 with minimal trophies

**Result:** 8th place finishes, Europa League, trophy drought.

**Lesson:** Pay your Sport Scientists. Always.

---

## 🛠️ Technologies Used

- **Python 3.10+** - Programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Matplotlib & Seaborn** - Data visualization
- **Plotly** - Interactive visualizations
- **Streamlit** - Web dashboard framework
- **Scikit-learn** - Machine learning models
- **Jupyter** - Interactive notebooks

---

## 🤝 Contributing

This is a personal portfolio project, but suggestions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Note:** Please maintain the Liverpool bias and United roasting spirit! 😄

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Abdullah Hasan Dafa**
- 📧 Email: dafa.abdullahhasan@gmail.com
- 🔗 GitHub: [@hasandafa](https://github.com/hasandafa)
- 📝 Blog: Substack article coming soon

---

## 🎓 Acknowledgments

- **Jürgen Klopp** - For showing the world how data-driven football should be done
- **Liverpool FC** - For 6 European Cups and consistent excellence
- **Sport Scientists** - The unsung heroes of modern football
- **Manchester United** - For providing endless comedy material and cautionary tales

---

## 📊 Project Stats

- **Lines of Code:** 10,000+
- **Data Points:** 50,000+
- **Visualizations:** 100+
- **Notebooks:** 6
- **Dashboard Pages:** 7
- **United Roasts:** Countless
- **Liverpool Pride:** Maximum

---

## 🔴 Final Message

> **Football is about data, Sport Science, and intelligent decision-making.**
> 
> Liverpool proves this with 6 European Cups.
> United disproves this with £1B+ spent for 8th place.
>
> **Choose your path wisely.**

### YNWA - You'll Never Walk Alone ⚽🔴

---

## 📞 Contact & Support

**Questions or feedback?**
- Open an issue on GitHub
- Email: dafa.abdullahhasan@gmail.com
- Star ⭐ this repo if you found it helpful!

**Remember:** Pay your Sport Scientists! 🧪📊⚽

---

<div align="center">

**Built with ❤️ for Liverpool FC**

**Built with 📊 for Data Science**

**Built with 😂 for United Mockery**

[![Liverpool FC](https://img.shields.io/badge/Liverpool_FC-You'll_Never_Walk_Alone-C8102E?style=for-the-badge&logo=liverpool)](https://www.liverpoolfc.com)

</div>




