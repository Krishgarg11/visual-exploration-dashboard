# ☕ Executive Café Sales Analytics & Interactive Dashboard Suite

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Express-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> A rigorous, portfolio-grade Data Analytics project transforming daily café chain sales records into an end-to-end intelligence suite. Includes statistical exploratory data analysis (EDA), anomaly and outlier auditing, multi-panel interactive Plotly subplots, a production-ready Streamlit analytical web app, and an executive decision memo.

---

## 📌 Executive Summary

This project evaluates the FY 2025 commercial performance of an expanding retail café chain across three Indian metropolitan outlets: **Pune**, **Jaipur**, and **Kochi**. Analyzing 3,285 raw daily records covering three core categories (**Beverages**, **Bakery**, **Merchandise**) and six promotional discount tiers (**0% to 25%**), the analysis establishes seasonal baselines, measures weekly footfall elasticity, uncovers promotional yield dynamics, and implements rigorous statistical outlier auditing.

### Key Commercial Highlights (FY 2025):
* **Audited Network Revenue:** **₹920.6 Million** across 3,282 verified operating records.
* **Average Transaction Line Yield:** **₹281 Thousand** per item-outlet day.
* **Top-Grossing Market:** **Pune** leading the network at **₹336.5 Million** (~36.6% market share).
* **Core Anchor Category:** **Beverages** driving **₹467.2 Million** (>50% of aggregate revenue).
* **Seasonal December Uplift:** **+27.5% MoM** surge over November (reaching ₹102.9 Million).
* **Weekend Premium:** Steady **+34.8% to +35.1%** revenue surge on Saturdays and Sundays across all categories.

---

## 📁 Repository Architecture

```text
visual-exploration-dashboard/
│
├── data/
│   ├── cafe_sales.csv            # Original synthetic dataset with intentional errors (3,285 rows)
│   └── cafe_clean.csv            # Cleaned, audited dataset (3,282 rows)
│
├── notebooks/
│   └── Visual_Exploration_and_Interactive_Dashboards.ipynb  # End-to-end reproducible analysis
│
├── reports/
│   ├── cafe_dashboard.html       # Standalone 2x2 interactive Plotly dashboard
│   ├── outlets_and_beverages.html# Standalone 1x2 comparative dashboard (Your Turn 7)
│   └── business_report.md        # One-page executive business memo with recommendations
│
├── app.py                        # Production-ready interactive Streamlit analytical application
├── requirements.txt              # Pinned environment dependencies
├── README.md                     # Comprehensive technical documentation & portfolio guide
└── .gitignore                    # Version control exclusion rules
```

---

## 🔍 Data Architecture & Outlier Audit Methodology

### 1. Synthetic Data Specification & Reproducibility
The dataset is generated using a fixed random seed (`21`) to guarantee 100% computational reproducibility across platforms:
* **Date Range:** 1 January 2025 to 31 December 2025 (365 calendar days).
* **Regional Outlets:** Pune, Jaipur, Kochi (3 outlets).
* **Product Lines:** Beverages (base ₹300k), Bakery (base ₹180k), Merchandise (base ₹90k).
* **Promotional Discount Tiers:** 0%, 5%, 10%, 15%, 20%, 25%.
* **Operational Multipliers:** 
  * Winter seasonality: $1.25\times$ (December and January)
  * Weekend premium: $1.35\times$ (Saturday and Sunday)
  * Annual trend growth: $1 + \frac{\text{day}}{365} \times 0.25$
  * Regional factors: Pune ($1.10\times$), Kochi ($1.00\times$), Jaipur ($0.95\times$)
  * Stochastic disturbance: $\mathcal{N}(1.0, 0.07)$

### 2. Outlier Investigation & Audit Decision
The raw dataset intentionally embeds three clerical data-entry transcription slips (multiplied by 7x):
* **Index 300 (2025-02-03, Jaipur, Beverages):** Reported ₹2,441.6k (Normal: ~₹340k)
* **Index 1800 (2025-07-20, Pune, Beverages):** Reported ₹3,294.2k (Normal: ~₹470k)
* **Index 2900 (2025-11-19, Pune, Merchandise):** Reported ₹1,055.6k (Normal: ~₹150k)

#### The Statistical Rule Evaluation:
* **The Methodological Flaw of Outlet-Level Grouping:** Applying an outlet-level threshold (`Revenue <= 3 × Outlet Mean`) removed **7 records**. Because Beverages generates over $3\times$ the volume of Merchandise, an outlet average blurs distinct item distributions, falsely flagging four genuine high-demand winter weekend days (e.g., Pune Beverages on 28 December at ₹959.5k).
* **The Item-Level Solution:** Applying an item-specific threshold (`Revenue <= 3 × Item Mean`) compares *like with like*, cleanly excising **exactly the 3 clerical errors** while preserving authentic winter weekend sales surges:
  $$\text{Raw Rows: } 3,285 \quad \longrightarrow \quad \text{Excised: } 3 \quad \longrightarrow \quad \text{Cleaned Rows: } 3,282$$

---

## 📊 Core Analytical Findings

### 1. Temporal Seasonality & Footfall Elasticity
* **The Winter Demand Curve:** Sales trough in February (₹64.6M) and steadily climb across spring and summer, culminating in a sharp winter surge in December (₹102.9M). December delivers **+27.5% MoM** growth over November (₹80.7M).
* **The Weekend Premium:** Saturday (₹341.0k) and Sunday (₹350.8k) generate an average of **₹345.9k** per line vs. **₹256.6k** on weekdays—a **+34.8% lift**.
* **Merchandise Weekend Elasticity:** Merchandise alone delivers a **+34.8% weekend lift** (₹164.3k vs ₹121.9k), proving that the weekend uplift is driven by overall footfall rather than category-specific consumption.

### 2. Multi-Category Cross Tabulation (Pivot Heatmaps)
* **Pune’s Market Leadership:** Pune leads in every single menu category:
  * Beverages: **₹488k** (vs ₹438k in Kochi, ₹415k in Jaipur)
  * Bakery: **₹288k** (vs ₹262k in Kochi, ₹249k in Jaipur)
  * Merchandise: **₹146k** (vs ₹131k in Kochi, ₹125k in Jaipur)
* **Category Rank Stability:** The ranking **Beverages > Bakery > Merchandise** is invariant across all geographic markets.
* **Granular Anomaly Detection:** In 11 out of 12 months, the regional order is strictly Pune > Kochi > Jaipur. However, in **February**, Jaipur (₹256.0k) slightly outperformed Kochi (₹242.0k), cautioning analysts against uncritically assuming absolute uniformity.

### 3. Promotional Elasticity (Association vs. Causation)
* Higher offers associate with higher average sales line revenues up to 20% (₹253.2k at 0% vs. ₹305.7k at 20%).
* **Marginal Return Collapse at 25%:** Moving from 20% to 25% produces a **negative marginal return (-₹1.1k)** across the chain (₹305.7k $\rightarrow$ ₹304.7k), while eroding margin.
* *Econometric Caveat:* We report this as an *association*, not direct causation, since promotional calendars coincide with high-volume weekend and holiday dates.

---

## 💻 Interactive Streamlit Application (`app.py`)

The Streamlit web application converts the analytical pipeline into a dynamic, production-grade decision dashboard.

### Core Features:
1. **Dynamic Sidebar Filters:**
   * Multi-select for Outlets (Pune, Jaipur, Kochi).
   * Multi-select for Product Categories (Beverages, Bakery, Merchandise).
   * Dual-handle Month Range Slider (Month 1 to 12).
   * Dual-handle Offer Discount Slider (0% to 25% in 5% increments).
   * One-click "Reset All Filters" button.
2. **Dynamic Headline KPI Metrics Cards:**
   * **Total Revenue (₹ Millions)** with formatted number display.
   * **Average Revenue per Line (₹ Thousands)**.
   * **Active Records Count** with benchmark comparison.
   * **Leading Regional Outlet** dynamically identifying the highest-grossing city.
   * **Top Product Line** tracking category contribution.
3. **Responsive 2x2 Plotly Grid:**
   * Chart A: Monthly revenue trajectory by outlet with unified hover cursor.
   * Chart B: Total cumulative revenue by category.
   * Chart C: Outlet vs. Category revenue yield heatmap.
   * Chart D: Average revenue yield across promotional offer tiers.
4. **Data Exploration & Export Drawer:**
   * Expandable underlying data table with active filter telemetry.
   * Direct CSV export button generating downloadable slices.
5. **Defensive Programming:**
   * Graceful empty-selection handling via `st.warning()` and `st.stop()`.
   * Caching via `@st.cache_data` for sub-second query latency.

---

## 🚀 Getting Started & Execution Guide

### Prerequisites
* Python 3.9+ (Tested on Python 3.11)
* Git

### 1. Installation
Clone the repository and install dependencies:
```bash
# Clone the repository
git clone https://github.com/your-username/visual-exploration-dashboard.git
cd visual-exploration-dashboard

# Create and activate a virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Running the Jupyter Notebook
Open and run the notebook top-to-bottom:
```bash
jupyter notebook notebooks/Visual_Exploration_and_Interactive_Dashboards.ipynb
```
*All cells are pre-executed with embedded interactive charts, tables, and assertion benchmarks.*

### 3. Launching the Interactive Streamlit App
Launch the web server locally:
```bash
streamlit run app.py
```
The application will automatically launch in your default web browser at `http://localhost:8501`.

### 4. Viewing the Standalone Plotly Dashboards
Open the pre-rendered HTML dashboards directly in Google Chrome, Edge, Safari, or Firefox without requiring Python:
```bash
# Windows
start reports/cafe_dashboard.html
start reports/outlets_and_beverages.html

# macOS
open reports/cafe_dashboard.html
open reports/outlets_and_beverages.html

# Linux
xdg-open reports/cafe_dashboard.html
```

---

## 🧪 Validation & Benchmark Verification

The repository includes strict programmatic assertions verifying data integrity against expected baselines:

| Metric / Scenario | Expected Target | Actual Result | Verification Status |
| :--- | :---: | :---: | :---: |
| **Raw Dataset Records** | 3,285 | 3,285 | ✅ Passed |
| **Audited Clean Records** | 3,282 | 3,282 | ✅ Passed |
| **Clerical Errors Excised** | Exactly 3 rows | Exactly 3 rows | ✅ Passed |
| **Total Cleaned Revenue** | ₹920.6 Million | ₹920.6 Million | ✅ Passed |
| **Pune Nov & Dec Sub-filter** | 182 rows, ₹66.2M | 182 rows, ₹66.2M | ✅ Passed |
| **Offer 20%–25% Sub-filter** | 1,079 rows, ₹326.4M | 1,079 rows, ₹326.4M | ✅ Passed |
| **Leading Outlet Overall** | Pune | Pune | ✅ Passed |
| **Leading Outlet (Offer 20–25%, No Pune)** | Kochi (712 rows, ₹205.0M) | Kochi (712 rows, ₹205.0M) | ✅ Passed |

---

## 📸 Visual Gallery & Application Screenshots

### 1. Executive Streamlit Dashboard Interface (`app.py`)
![Executive Streamlit Dashboard Interface](assets/streamlit_dashboard_preview.png)
*Live web application featuring adaptive styling, high-contrast KPI metric cards with context badges, multi-attribute sidebar filters, and synchronized Plotly visualizations.*

### 2. Multi-Panel 2x2 Interactive Plotly Dashboard (`reports/cafe_dashboard.html`)
![Plotly Subplot Dashboard](assets/cafe_dashboard_preview.png)
*Standalone 2x2 Plotly canvas with direct data labels on bars, unified hover tooltips, and unstacked monthly trajectories.*

### 3. Outlet Performance & Beverage Trajectory Comparative Dashboard (`reports/outlets_and_beverages.html`)
![Comparative Dashboard](assets/outlets_and_beverages_preview.png)
*Side-by-side executive view visualizing total annual revenue by regional outlet alongside the monthly beverage expansion trajectory (Your Turn 7).*

---

## 🎯 Recruiter & Interview Demonstration Notes

When presenting this project during a technical interview or portfolio review:
1. **Highlight the Outlier Auditing Discipline:** Emphasize why simple statistical clipping (like standard deviation or outlet-level grouping) would have discarded valid business signals (winter holiday surges). Explain the three-step audit framework (plausibility, operational cause, verification).
2. **Demonstrate Economic Sensitivity:** Walk through the offer analysis, showing how moving from 20% to 25% discount yields flat-to-negative revenue change, illustrating business acumen over naive correlation.
3. **Showcase Modern Tooling:** Demonstrate both the standalone offline deliverable (`cafe_dashboard.html` for stakeholders without Python) and the live application (`app.py` for exploratory self-service).

---

## 📜 License
This project is open-source and licensed under the [MIT License](LICENSE).
