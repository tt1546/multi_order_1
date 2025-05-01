import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Multi Order Analysis", layout="wide")
st.title("Multi Order Analysis")
# Sidebar navigation with emoji icons
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/684/684908.png", width=80)
    st.markdown("## Navigation")
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_Customer_Clustering.py", label="👥 Customer Clustering")
    st.page_link("pages/2_Multi_Order_Analysis.py", label="📊 Multi-Order Analysis")
    st.page_link("pages/3_Temporal_Pattern_Exploration.py", label="📈 Temporal Pattern Exploration")
    st.page_link("pages/4_Fulfillment_Cost_Analysis.py", label="📦 Fulfillment Cost")
    st.page_link("pages/5_Model_Predictor.py", label="🤖 Predictor")
    st.markdown("---")
    st.caption("Built by Group 13")
st.divider()

# ---------------------------------------- #
# 🔹 Chart 1: Multi-Order Ratio by Option
# ---------------------------------------- #
st.subheader("Multi-Order Ratio by Option")

st.markdown(
    """
**Purpose:**  
To evaluate which service/product options are more likely to be repeated by customers. A higher multi-order ratio may reflect better customer stickiness or suitability for repeat use.
    """
)

# Load option_comparison data from CSV
option_comparison = pd.read_csv("data/option_comparison.csv")

# Create chart
fig1 = px.bar(
    option_comparison,
    x='option_id',
    y='multi_order_ratio',
    text=option_comparison['multi_order_ratio'].round(2),
    title='Multi-Order Ratio by Option',
    labels={'option_id': 'Option ID', 'multi_order_ratio': 'Multi-Order Ratio'},
)

# Customize layout
fig1.update_traces(marker_color='skyblue', textposition='outside')
fig1.update_layout(
    xaxis_tickangle=-45,
    xaxis_tickfont_size=10,
    yaxis_range=[0, option_comparison['multi_order_ratio'].max() * 1.1],
    plot_bgcolor='white',
    yaxis_gridcolor='lightgray',
    margin=dict(t=60, b=80, l=60, r=30)
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    """
**Observations:**

- **Option_15** has the highest multi-order ratio at **0.16**, significantly above the rest, suggesting strong customer loyalty or repeated purchasing behavior.
- The next group of top-performing options (e.g., **Option_3, Option_12, Option_2**) all share similar multi-order ratios around **0.14**.
- The multi-order ratio gradually declines across options, with the **lowest values observed in Option_9 and Option_8**, at **0.09** and **0.08**, respectively.
- The chart shows a relatively smooth distribution without sharp drops, indicating a **progressive differentiation** in repeat-order preference across options.
    """
)

st.divider()

# ---------------------------------------- #
# 🔹 Chart 2: Top Purchased Options by Customer Cluster
# ---------------------------------------- #
st.subheader("Top Purchased Options by Customer Cluster")

st.markdown(
    """
**Purpose:**  
To identify the most preferred options across different customer segments, allowing us to understand variation in product preferences and improve cluster-specific marketing strategies.
    """
)

# Load top option data from CSV
top_option_per_cluster = pd.read_csv("data/top_option_per_cluster.csv")

# Ensure cluster is string for color mapping
top_option_per_cluster['cluster'] = top_option_per_cluster['cluster'].astype(str)

# Define cluster colors
cluster_colors = {
    '0': 'red',
    '1': 'yellow',
    '2': 'blue'
}

# Create chart
fig2 = px.bar(
    top_option_per_cluster,
    x='order_count',
    y='option_id',
    color='cluster',
    color_discrete_map=cluster_colors,
    orientation='h',
    barmode='group',
    title='Top 10 Purchased Options by Customer Cluster',
    labels={'order_count': 'Purchase Quantity', 'option_id': 'Option ID', 'cluster': 'Cluster'},
)

# Customize layout
fig2.update_layout(
    bargap=0.4,
    plot_bgcolor='white',
    xaxis_gridcolor='lightgray',
    yaxis=dict(categoryorder='total ascending'),
    legend_title_text='Cluster'
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
**Observations:**

- **Cluster 2 (darkest bars)** consistently dominates purchase volume across all top 10 options, indicating a **higher engagement or purchasing power**.
- Options **Option_1** and **Option_20** are the most purchased overall, with Cluster 2 contributing significantly more than Clusters 0 and 1.
- Cluster **0 (lightest bars)** and **1** follow similar purchasing patterns, but their volumes are generally lower, especially for **Option_3**, **Option_17**, and **Option_5**, where Cluster 2's purchases are nearly double.
- Despite being lower in total quantity, Clusters 0 and 1 show more balanced interest across the option set (e.g., **Option_15** and **Option_6**), suggesting **preference diversity**.
- These distinctions provide a strong basis for **cluster-specific product targeting** and **inventory planning**.
    """
)
