import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Fulfillment Cost Analysis", layout="wide")
st.title("Fulfillment Cost Analysis")

# Load data
df_path = "data/cluster_simulation_df.csv"
cluster_simulation_df = pd.read_csv(df_path)
st.divider()
# ---------------------------------------- #
# Section: Delivery Cost Comparison
# ---------------------------------------- #
st.subheader("Delivery Cost Comparison")

st.markdown(
    """
**Purpose:**  
To evaluate the total cost savings achieved by merging deliveries of multiple orders into a single shipment.
    """
)

# Display metrics
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Estimated Savings Rate", value="27.4%")
with col2:
    st.metric(label="Estimated Savings Amount", value="¥99,153")

# Cost chart
original_cost = 362238
merged_total_cost = 263085
costs = [original_cost, merged_total_cost]
labels = ['Original Cost', 'Merged Cost']
colors = ['#4C72B0', '#55A868']

fig = go.Figure(data=[
    go.Bar(
        x=labels,
        y=costs,
        marker_color=colors,
        text=[f'{c:,.0f}' for c in costs],
        textposition='outside'
    )
])
fig.update_layout(
    title='Delivery Cost Comparison: Original vs Merged',
    yaxis_title='Total Cost (Yuan)',
    plot_bgcolor='white',
    yaxis_gridcolor='lightgray'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**Observations:**  
Merging deliveries results in an overall cost reduction of about **¥99,153**, representing a **27.4%** decrease in fulfillment costs.
    """
)

st.divider()

# ---------------------------------------- #
# Section: Saving Amount per Cluster
# ---------------------------------------- #
st.subheader("Saving Amount by Customer Cluster")

st.markdown(
    """
**Purpose:**  
To examine how much cost is saved in absolute terms across different customer clusters when merged delivery is applied.
    """
)

fig1 = px.bar(
    cluster_simulation_df,
    x='cluster_id',
    y='saving_amount',
    title='Saving Amount per Cluster',
    labels={'cluster_id': 'Cluster ID', 'saving_amount': 'Saving Amount (¥)'},
    color_discrete_sequence=['skyblue']
)
fig1.update_layout(
    plot_bgcolor='white',
    yaxis_gridcolor='lightgray',
    title_font=dict(size=18),
    yaxis_title_font=dict(size=14)
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    """
**Observations:**  
Some customer clusters contributed to significantly more cost savings than others. One cluster achieved over **¥50,000** in reduction alone, likely due to high frequency or spatial concentration of orders.
    """
)

st.divider()

# ---------------------------------------- #
# Section: Saving Rate per Cluster
# ---------------------------------------- #
st.subheader("Saving Rate by Customer Cluster")

st.markdown(
    """
**Purpose:**  
To evaluate which customer segments benefit most in relative terms from delivery merging, revealing which clusters are most efficient to consolidate.
    """
)
cluster_simulation_df['saving_rate'] = cluster_simulation_df['saving_rate'] * 100  # 若为比例

fig2 = px.bar(
    cluster_simulation_df,
    x='cluster_id',
    y='saving_rate',
    title='Saving Rate per Cluster',
    labels={'cluster_id': 'Cluster ID', 'saving_rate': 'Saving Rate (%)'},
    color_discrete_sequence=['salmon']
)
fig2.update_layout(
    plot_bgcolor='white',
    yaxis_gridcolor='lightgray',
    title_font=dict(size=18),
    yaxis_title_font=dict(size=14)
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
**Observations:**  
Across clusters, the saving rate varies but consistently shows double-digit percentages. Some clusters achieved over **30% reduction**, highlighting the potential for cluster-specific delivery optimization.
    """
)

st.divider()

# ---------------------------------------- #
# Section: Summary
# ---------------------------------------- #
st.markdown(
    """
### Summary

- On average, consolidating multi-order deliveries can save approximately **25–28%** of fulfillment costs.
- Cluster-specific analysis reveals significant differences: some segments achieve up to **¥50k** in savings.
- These findings support data-driven logistics strategies such as cluster-based routing and priority batch scheduling.
    """
)
