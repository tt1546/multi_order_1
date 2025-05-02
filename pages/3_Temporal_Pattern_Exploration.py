import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Temporal Pattern Exploration", layout="wide")
st.title("Temporal Pattern Exploration")
st.divider()
# ---------------------------------------- #
# Hourly Multi-Order Trend
# ---------------------------------------- #
st.subheader("Hourly Multi-Order Trend")

st.markdown(
    """
**Purpose:**  
To identify intra-day patterns in repeat ordering behavior, such as peak times and low-activity periods.
    """
)

# Load hourly stats
hourly_stats = pd.read_csv("data/hourly_stats.csv")
hourly_stats = hourly_stats.sort_values("order_hour")

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Bar(
        x=hourly_stats["order_hour"],
        y=hourly_stats["sum"],
        name="Multi-Order Count",
        marker_color="skyblue",
        opacity=0.7
    ),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(
        x=hourly_stats["order_hour"],
        y=hourly_stats["multiorder_ratio"],
        name="Multi-Order Ratio",
        line=dict(color="orange", width=2),
        mode="lines+markers"
    ),
    secondary_y=True
)

fig.update_layout(
    title="Hourly Multi-Order Count and Ratio",
    xaxis_title="Hour of Day",
    xaxis=dict(tickvals=list(range(24))),
    plot_bgcolor="white",
    hovermode="x unified",
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    )
)
fig.update_yaxes(
    title_text="Multi-Order Count",
    secondary_y=False,
    showgrid=True,
    gridcolor="lightgray",
    gridwidth=1
)
fig.update_yaxes(
    title_text="Multi-Order Ratio",
    secondary_y=True,
    showgrid=False
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**Observations:**

- Multi-order count (blue bars) shows two main peaks: one at **11:00** and another in the **late evening (21:00–23:00)**.
- The **multi-order ratio** (orange line) spikes sharply at **4:00**, despite the low absolute order volume at that hour.
- During **midnight to early morning (0:00–6:00)**, although the overall volume is relatively low, the multi-order ratio remains elevated, suggesting that **a higher proportion of orders during this period are repeat orders**.
- In contrast, during **afternoon hours (13:00–16:00)**, both the count and the ratio dip slightly before rising again in the evening.
    """
)

st.divider()

# ---------------------------------------- #
# Weekly Multi-Order Trend
# ---------------------------------------- #
st.subheader("Weekly Multi-Order Trend")

st.markdown(
    """
**Purpose:**  
To explore day-of-week patterns in customer repeat ordering behavior, identifying weekday or weekend effects.
    """
)

# Load weekly stats
weekly_stats = pd.read_csv("data/weekly_stats.csv")
weekday_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekly_stats['weekday_name'] = pd.Categorical(weekly_stats['weekday_name'], categories=weekday_order, ordered=True)
weekly_stats = weekly_stats.sort_values("weekday_name")

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=weekly_stats["weekday_name"],
        y=weekly_stats["sum"],
        name="Multi-Order Count",
        marker_color="skyblue",
        opacity=0.8
    )
)
fig.add_trace(
    go.Scatter(
        x=weekly_stats["weekday_name"],
        y=weekly_stats["multiorder_ratio"],
        name="Multi-Order Ratio",
        line=dict(color="orange", width=2),
        mode="lines+markers",
        yaxis="y2"
    )
)
fig.update_layout(
    title="Multi-Order Count and Ratio by Day of the Week",
    xaxis_title="Day of Week",
    yaxis=dict(
        title="Multi-Order Count",
        title_font_color="skyblue",
        gridcolor="lightgray",
        griddash="dot"
    ),
    yaxis2=dict(
        title="Multi-Order Ratio",
        title_font_color="orange",
        overlaying="y",
        side="right"
    ),
    plot_bgcolor="white",
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**Observations:**

- Multi-order counts (blue bars) peak midweek, especially on **Wednesday** and **Thursday**, both exceeding **1,450** orders.
- The **multi-order ratio** (orange line) also reaches its highest values on **Tuesday, Wednesday, and Thursday**, all above **0.135**.
- The **lowest multi-order count and ratio** are observed on **Sunday**, where the ratio dips to approximately **0.112**, and the count is below **1,000**.
- There is a **clear weekday preference**, with higher multi-order activity and repeat behavior occurring from **Tuesday to Thursday**, and a gradual decline into the weekend.
    """
)

st.divider()

# ---------------------------------------- #
# Daily Multi-Order Trend
# ---------------------------------------- #
st.subheader("Daily Multi-Order Trend")

st.markdown(
    """
**Purpose:**  
To reveal long-term temporal patterns in customer repeat behavior, including seasonal cycles or marketing-driven effects.
    """
)

# Load daily stats
annual_stats = pd.read_csv("data/annual_stats.csv", parse_dates=["order_date"])
annual_stats.set_index("order_date", inplace=True)

start_date = annual_stats.index.min()
end_date = annual_stats.index.max()


apply_filter = st.checkbox("Enable Date Filter", value=True)


if apply_filter:
    date_range = st.date_input(
        "Select Date Range:",
        value=(start_date, end_date),
        min_value=start_date,
        max_value=end_date
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:

        filtered_stats = annual_stats.loc[date_range[0]:date_range[1]]
    else:
        st.warning("Please select both start and end dates.")
        filtered_stats = pd.DataFrame()  
else:
    filtered_stats = annual_stats.copy()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=filtered_stats.index,
    y=filtered_stats["multiorder_ratio"],
    name="Daily Multi-Order Ratio",
    line=dict(color="gray", width=1),
    mode="lines",
    opacity=0.5  
))

if "multiorder_ratio_smooth" in filtered_stats.columns:
    fig.add_trace(go.Scatter(
        x=filtered_stats.index,
        y=filtered_stats["multiorder_ratio_smooth"],
        name="7-Day Moving Avg",
        line=dict(color="orange", width=2),  
        mode="lines"
    ))


fig.update_layout(
    title="Daily Multi-Order Ratio Over Time",
    xaxis_title="Date",
    yaxis_title="Multi-Order Ratio",
    plot_bgcolor="white",
    legend_title_text="Legend"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**Observations:**

- The multi-order ratio (gray line) shows considerable daily fluctuations, but the 7-day moving average (orange line) reveals a **clear seasonal trend**.
- In each of the years shown (2021, 2022, 2023), the **multi-order ratio peaks consistently around November**.
- The ratio **declines sharply during the year-end period (December to January)**, suggesting lower repeat purchase behavior during holidays or post-holiday slumps.
- The 7-day smoothed line shows that **overall yearly patterns repeat**, indicating possible **cyclical customer behavior** linked to seasonal factors such as promotions or demand cycles.
    """
)
