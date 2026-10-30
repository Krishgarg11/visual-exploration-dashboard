import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import pathlib

# ==============================================================================
# 1. PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="Executive Café Sales Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive polish (adaptive for light/dark themes)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.0rem;
        color: #64748b;
        margin-bottom: 1.4rem;
        line-height: 1.5;
    }
    
    div[data-testid="metric-container"] {
        background-color: rgba(248, 250, 252, 0.7);
        border: 1px solid rgba(226, 232, 240, 0.9);
        padding: 1.0rem 1.1rem;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px -1px rgba(0,0,0,0.08);
        border-color: #94a3b8;
    }
    
    div[data-testid="metric-container"] label {
        font-size: 0.80rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.80rem !important;
        font-weight: 700 !important;
    }

    .stPlotlyChart {
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        padding: 0.4rem;
    }
    
    .filter-summary-card {
        background-color: rgba(241, 245, 249, 0.6);
        border-left: 4px solid #2563eb;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DATA INGESTION & CACHING
# ==============================================================================
@st.cache_data
def load_data():
    current_dir = pathlib.Path(__file__).resolve().parent if "__file__" in globals() else pathlib.Path.cwd()
    candidates = [
        current_dir / "data" / "cafe_clean.csv",
        current_dir / "cafe_clean.csv",
        pathlib.Path("visual-exploration-dashboard/data/cafe_clean.csv").resolve(),
        pathlib.Path("data/cafe_clean.csv").resolve(),
        pathlib.Path("cafe_clean.csv").resolve(),
    ]
    for p in candidates:
        if p.exists():
            df = pd.read_csv(p, parse_dates=["Date"])
            if "Month" not in df.columns:
                df["Month"] = df["Date"].dt.month
            if "Weekday" not in df.columns:
                df["Weekday"] = df["Date"].dt.dayofweek
            return df
    raise FileNotFoundError(f"Could not find cafe_clean.csv. Checked: {[str(c) for c in candidates]}")

df = load_data()

# ==============================================================================
# 3. SIDEBAR FILTERS (Preserving all PDF & Your Turn 8 Requirements)
# ==============================================================================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600&auto=format&fit=crop&q=80", 
        caption="Café Chain Operations Analytics",
        use_container_width=True
    )
    
    st.header("⚙️ Dashboard Controls")
    st.caption("Filter records by regional store, menu category, date window, or discount tiers.")
    
    all_outlets = sorted(df["Outlet"].unique().tolist())
    all_items = sorted(df["Item"].unique().tolist())
    
    # Reset filters helper
    if st.button("🔄 Reset All Filters", key="reset_filters", use_container_width=True):
        st.session_state["filter_outlets"] = all_outlets
        st.session_state["filter_items"] = all_items
        st.session_state["filter_months"] = (1, 12)
        st.session_state["filter_offers"] = (0, 25)
    
    selected_outlets = st.multiselect(
        "Select Outlets:",
        options=all_outlets,
        default=st.session_state.get("filter_outlets", all_outlets),
        key="filter_outlets",
        help="Select one or more regional outlets."
    )
    
    selected_items = st.multiselect(
        "Select Product Categories:",
        options=all_items,
        default=st.session_state.get("filter_items", all_items),
        key="filter_items",
        help="Select menu product categories."
    )
    
    month_range = st.slider(
        "Month Window (1 = Jan, 12 = Dec):",
        min_value=1,
        max_value=12,
        value=st.session_state.get("filter_months", (1, 12)),
        key="filter_months",
        help="Select monthly time window."
    )
    
    offer_range = st.slider(
        "Promotional Offer Range (%):",
        min_value=0,
        max_value=25,
        step=5,
        value=st.session_state.get("filter_offers", (0, 25)),
        key="filter_offers",
        help="Select discount offer levels (0% to 25%)."
    )
    
    st.divider()
    st.markdown("**Data Integrity Note**")
    st.caption("Clean dataset excludes 3 confirmed data-entry transcription errors (7x multiplier anomalies). Legitimate winter and weekend peaks are preserved.")

# ==============================================================================
# 4. FILTERING LOGIC & VALIDATION
# ==============================================================================
view = df[
    df["Outlet"].isin(selected_outlets)
    & df["Item"].isin(selected_items)
    & df["Month"].between(month_range[0], month_range[1])
    & df["Offer"].between(offer_range[0], offer_range[1])
]

# Guard clause for empty view
if view.empty:
    st.warning("⚠️ No records match the selected filter criteria. Please broaden your selection in the sidebar.")
    st.stop()

# ==============================================================================
# 5. HEADER & EXECUTIVE KPIS
# ==============================================================================
st.markdown('<div class="main-header">☕ Executive Café Sales & Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive visual analytics platform monitoring revenue streams, seasonal fluctuations, and promotional sensitivity across regional outlets (FY 2025).</div>', unsafe_allow_html=True)

# Calculation of KPIs
total_rev_million = view["Revenue"].sum() / 1000.0
avg_rev_thousand = view["Revenue"].mean()
rows_count = len(view)
best_outlet = view.groupby("Outlet")["Revenue"].sum().idxmax()
best_outlet_rev = view.groupby("Outlet")["Revenue"].sum().max() / 1000.0
top_item = view.groupby("Item")["Revenue"].sum().idxmax()
top_item_rev = view.groupby("Item")["Revenue"].sum().max() / 1000.0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(
    "Total Revenue", 
    f"₹{total_rev_million:,.1f} M", 
    delta=f"₹{view['Revenue'].sum():,.0f}k sum",
    help="Total cumulative revenue in millions of Indian Rupees."
)
col2.metric(
    "Average / Row", 
    f"₹{avg_rev_thousand:,.0f} k", 
    delta=f"Std: ₹{view['Revenue'].std():,.0f}k",
    delta_color="off",
    help="Average daily sales revenue per item-outlet record in thousands."
)
col3.metric(
    "Rows Displayed", 
    f"{rows_count:,}", 
    delta=f"{rows_count / len(df) * 100:.1f}% of total",
    delta_color="off",
    help="Count of daily transaction line items currently in view."
)
col4.metric(
    "Leading Outlet", 
    f"{best_outlet}", 
    delta=f"₹{best_outlet_rev:,.1f} M gross",
    help="Highest grossing outlet within current filter parameters."
)
col5.metric(
    "Top Product Line", 
    f"{top_item}", 
    delta=f"₹{top_item_rev:,.1f} M gross",
    help="Highest revenue-generating product category."
)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 6. CORE 2x2 INTERACTIVE PLOTLY VISUALIZATIONS
# ==============================================================================
chart_row1_col1, chart_row1_col2 = st.columns(2)

# --- Chart A: Monthly Revenue by Outlet ---
with chart_row1_col1:
    monthly_data = view.groupby(["Month", "Outlet"], as_index=False)["Revenue"].sum()
    fig_a = px.line(
        monthly_data,
        x="Month",
        y="Revenue",
        color="Outlet",
        markers=True,
        title="<b>Monthly Revenue Trajectory by Outlet</b>",
        labels={"Revenue": "Revenue (₹ thousand)", "Month": "Month of Year"},
        color_discrete_map={"Pune": "#2563eb", "Jaipur": "#ea580c", "Kochi": "#16a34a"}
    )
    for trace in fig_a.data:
        trace.hovertemplate = "<b>%{fullData.name}</b><br>Month: %{x}<br>Revenue: ₹%{y:,.1f}k<extra></extra>"
    fig_a.update_layout(
        template="simple_white",
        hovermode="x unified",
        margin=dict(l=50, r=40, t=60, b=40),
        xaxis=dict(dtick=1, showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_a, use_container_width=True)

# --- Chart B: Total Revenue by Item ---
with chart_row1_col2:
    by_item_data = view.groupby("Item", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    fig_b = px.bar(
        by_item_data,
        x="Item",
        y="Revenue",
        color="Item",
        text=by_item_data["Revenue"].apply(lambda v: f"₹{v/1000:,.1f}M"),
        title="<b>Total Revenue by Product Category</b>",
        labels={"Revenue": "Cumulative Revenue (₹ thousand)", "Item": "Product Line"},
        color_discrete_sequence=["#2563eb", "#6366f1", "#06b6d4"]
    )
    fig_b.update_traces(
        textposition="outside",
        hovertemplate="Category: <b>%{x}</b><br>Total: ₹%{y:,.1f}k<extra></extra>"
    )
    fig_b.update_layout(
        template="simple_white",
        margin=dict(l=50, r=40, t=60, b=40),
        showlegend=False,
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9")
    )
    st.plotly_chart(fig_b, use_container_width=True)

chart_row2_col1, chart_row2_col2 = st.columns(2)

# --- Chart C: Average Revenue Outlet vs Item Heatmap ---
with chart_row2_col1:
    grid = view.pivot_table(index="Outlet", columns="Item", values="Revenue", aggfunc="mean")
    fig_c = px.imshow(
        grid,
        text_auto=".0f",
        color_continuous_scale="Blues",
        title="<b>Average Transaction Value: Outlet vs Category</b>",
        labels=dict(color="Avg Rev (₹ k)")
    )
    fig_c.update_traces(
        hovertemplate="Outlet: <b>%{y}</b><br>Category: <b>%{x}</b><br>Average: ₹%{z:.1f}k<extra></extra>"
    )
    fig_c.update_layout(
        template="simple_white",
        margin=dict(l=50, r=40, t=60, b=40)
    )
    st.plotly_chart(fig_c, use_container_width=True)

# --- Chart D: Average Revenue by Offer Level ---
with chart_row2_col2:
    by_offer_data = view.groupby("Offer", as_index=False)["Revenue"].mean()
    fig_d = px.bar(
        by_offer_data,
        x="Offer",
        y="Revenue",
        text=by_offer_data["Revenue"].apply(lambda v: f"₹{v:,.0f}k"),
        title="<b>Average Revenue Yield by Offer Tier (%)</b>",
        labels={"Revenue": "Average Revenue (₹ thousand)", "Offer": "Promotional Discount Level (%)"},
        color="Revenue",
        color_continuous_scale="Blues"
    )
    fig_d.update_traces(
        textposition="outside",
        hovertemplate="Discount Level: <b>%{x}%</b><br>Average Revenue: ₹%{y:,.1f}k<extra></extra>"
    )
    fig_d.update_layout(
        template="simple_white",
        margin=dict(l=50, r=40, t=60, b=40),
        coloraxis_showscale=False,
        xaxis=dict(tickmode="array", tickvals=[0, 5, 10, 15, 20, 25]),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9")
    )
    st.plotly_chart(fig_d, use_container_width=True)

# ==============================================================================
# 7. GRANULAR DATA PREVIEW & EXPORT FACILITY
# ==============================================================================
with st.expander("🔍 Explore Underlying Granular Dataset & Export"):
    st.markdown("### Active Selection Summary")
    st.markdown(
        f"""
        <div class="filter-summary-card">
            <b>Selected Markets:</b> {', '.join(selected_outlets)} &nbsp;|&nbsp; 
            <b>Categories:</b> {', '.join(selected_items)} &nbsp;|&nbsp; 
            <b>Period:</b> Month {month_range[0]} to {month_range[1]} &nbsp;|&nbsp; 
            <b>Discount Tiers:</b> {offer_range[0]}% to {offer_range[1]}% &nbsp;|&nbsp;
            <b>Active Line Items:</b> {len(view):,}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    tab_data, tab_stats = st.tabs(["📋 Filtered Transaction Records", "📊 Distribution & Summary Statistics"])
    
    with tab_data:
        st.dataframe(view, use_container_width=True, height=280)
        csv_bytes = view.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Dataset as CSV",
            data=csv_bytes,
            file_name="filtered_cafe_sales.csv",
            mime="text/csv",
            help="Export the currently filtered view to a CSV spreadsheet."
        )
        
    with tab_stats:
        st.markdown("**Revenue Distribution Statistics (₹ thousand):**")
        stats_df = view["Revenue"].describe().to_frame().T
        stats_df.columns = ["Count", "Mean (₹k)", "Std Dev", "Min", "25% (Q1)", "Median (50%)", "75% (Q3)", "Max"]
        st.dataframe(stats_df.round(1), use_container_width=True)

# Footer
st.markdown("---")
st.caption("Executive Café Sales Analytics Dashboard • Developed for Data Analytics Portfolio Demonstration • Built with Streamlit & Plotly")
