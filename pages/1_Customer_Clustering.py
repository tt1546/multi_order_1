import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Customer Clustering", layout="wide")
st.title("Customer Clustering")

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


# Load data
multi_order_stats = pd.read_csv("data/multi_order_stats.csv")
gmv_per_customer = pd.read_csv("data/gmv_per_customer.csv")
segment_distribution = pd.read_csv("data/segment_distribution.csv")
customer_profile = pd.read_csv("data/customer_profile.csv")
hotzone_customers = pd.read_csv("data/hotzone_customers.csv")

st.divider()
# Chart: fig1 - Multi-Order Ratio Distribution
fig1 = px.histogram(
    multi_order_stats,
    x='multi_order_ratio',
    nbins=30,
    title='Distribution of Multi-Order Ratio Among Customers',
    labels={'multi_order_ratio': 'Multi-Order Ratio (12h repeated orders)'}
)
fig1.update_layout(
    yaxis_title='Number of Customers',
    plot_bgcolor='white',
    yaxis=dict(gridcolor='rgba(0,0,0,0.1)', griddash='dot')
)
fig1.update_traces(marker_line_color='black', marker_line_width=1)

# Chart: fig2 - GMV Multi-Order Ratio
fig2 = px.histogram(
    gmv_per_customer,
    x='gmv_multi_order_ratio',
    nbins=30,
    title='Distribution Comparison: GMV Multi Order Ratio',
    labels={'gmv_multi_order_ratio': 'GMV Multi Order Ratio'},
    color_discrete_sequence=['skyblue'],
    opacity=0.8
)
fig2.update_layout(
    yaxis_title='Customer Count',
    plot_bgcolor='white',
    bargap=0.05,
    hovermode='x',
    xaxis_title_font_size=12,
    yaxis_title_font_size=12,
    title_pad=dict(t=20),
    legend_title_text='GMV Total',
    yaxis=dict(gridcolor='lightgray', gridwidth=1, griddash='dot', showgrid=True)
)
fig2.update_traces(marker_line_width=1, marker_line_color='black', hovertemplate='Ratio: %{x}<br>Count: %{y}', name='GMV Total')

# Chart: fig3 - Quantile Segment Bar
fig3 = px.bar(
    segment_distribution,
    x='customer_segment',
    y='customer_count',
    title='Multi-Order Ratio Distribution (Quantile-based)',
    labels={'customer_count': 'Number of Customers', 'customer_segment': 'Ratio Segment'},
    color_discrete_sequence=['skyblue']
)
fig3.update_layout(
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    plot_bgcolor='white',
    yaxis=dict(gridcolor='rgba(0,0,0,0.1)', gridwidth=1, griddash='dot')
)
fig3.update_traces(marker_line_width=1, marker_line_color='black')

st.divider()
st.subheader("Distribution of Multi-Order Ratio Among Customers")

st.markdown("""
**Purpose:**
To explore the overall distribution of repeat ordering behavior across customers based on 12-hour interval grouping.
""")

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
**Observations:**
- A noticeable peak exists at **0.0**, indicating that a large group of customers did not place repeated orders within 12 hours at all.
- Apart from the spike at 0, the distribution shows a **right-skewed** shape, with most customers falling between **0.05 and 0.2** in Multi-Order Ratio.
- Only a small number of customers have ratios exceeding **0.3**, suggesting that frequent short-term reordering is relatively rare.

**Preliminary Insights:**
- The large proportion of non-repeat customers suggests a potential for growth through **re-engagement or reminder strategies**.
- Customers in the **0.05–0.2** range could be targeted for **repeat order incentives**, as they show some tendency to reorder.
- A deeper segmentation of customers based on their Multi-Order Ratio can help identify **conversion opportunities** and tailor **retention campaigns**.
""")

st.divider()
st.subheader("GMV Multi-Order Ratio Distribution")

st.markdown("""
**Purpose:**
To compare GMV contribution of customers with varying levels of multi-order behavior.
""")

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
**Observations:**
- The distribution of GMV Multi Order Ratio is **right-skewed**, with most customers having a ratio between **0.05 and 0.25**.
- There is a peak around the **0.15 mark**, indicating that many customers generate about 15% of their total GMV from multi-orders within 12 hours.
- Only a small number of customers have GMV Multi Order Ratios exceeding **0.4**, suggesting that high-frequency high-value repeat behavior is relatively rare.
""")

st.divider()
st.subheader("Segment Distribution of Multi-Order Ratios")
st.markdown("""
**Purpose:**
To analyze how customers are distributed across different multi-order ratio segments based on quantiles.
""")

st.markdown("""
We segmented customers based on their 12-hour Multi-Order Ratio using the criteria shown below:
""")

# Define segment table data
segment_table = pd.DataFrame({
    "Segment Name": ["Very High", "High", "Medium", "Low"],
    "Multi-order Rate Range": [">= 0.30", "0.20 – 0.30", "0.10 – 0.20", "< 0.10"],
    "Description": [
        "Extremely high repeat ordering; ultra-loyal customers",
        "Strong preference for placing multiple orders within 12 hours (core users)",
        "Moderate repeat ordering; potential growth customers",
        "Infrequent 12-hour multi-orders; occasional customers"
    ]
})

# Display as styled table
st.dataframe(segment_table, use_container_width=True, hide_index=True)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
**Observations:**
- The majority of customers fall into the **Low** and **Medium** ratio segments, with both segments containing over 700 customers each.
- The **High** segment includes significantly fewer customers, indicating that frequent repeat behavior within 12 hours is less common.
- The **Very High** segment has the smallest customer count, showing that only a small subset of customers exhibit strong repeat-order tendencies.
""")

st.divider()
st.subheader("Customer Density Heatmap")

st.markdown("""
**Purpose:**
To visualize geographic concentration of customers for operational planning.
""")

plt.figure(figsize=(10, 8))
kde = sns.kdeplot(
    x=customer_profile['address_lon'],
    y=customer_profile['address_lat'],
    fill=True,
    cmap="YlOrRd",
    thresh=0.05,
    levels=100
)
plt.colorbar(kde.collections[0], label='Density')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Customer Density Heatmap')
plt.grid(True, linestyle='--', alpha=0.5)
st.pyplot(plt.gcf())
plt.clf()

st.markdown("""
**Observations:**
- The highest customer density is concentrated in the region around **longitude 103.7–103.8** and **latitude 1.32–1.36**, as indicated by the dark red zone in the heatmap.
- This central cluster suggests a **densely populated or commercially active area**, which may represent key urban neighborhoods or business hubs.
- The density gradually decreases moving outward, particularly toward the **eastern (longitude > 103.9)** and **southern (latitude < 1.30)** regions.
- The spatial pattern confirms that **logistics and marketing efforts** should be prioritized in the central high-density area to maximize impact.
""")
st.divider()
st.subheader("Hotzone Clusters (KMeans)")

st.markdown("""
**Purpose:**
To visualize spatial segmentation of customers using KMeans clustering.
""")

cluster_order = ['0', '1', '2']
cluster_colors = {'0': 'red', '1': 'yellow', '2': 'blue'}
fig4 = px.scatter(
    hotzone_customers,
    x='address_lon',
    y='address_lat',
    color='cluster',
    category_orders={'cluster': cluster_order},
    color_discrete_map=cluster_colors,
    title='Hotzone Customer Clusters (KMeans)',
    labels={'address_lon': 'Longitude', 'address_lat': 'Latitude'},
    opacity=0.6
)
fig4.update_layout(
    plot_bgcolor='white',
    legend_title_text='Cluster',
    xaxis=dict(showgrid=True, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridcolor='lightgray')
)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Cluster Summary Statistics")

cluster_summary = hotzone_customers.groupby('cluster').agg({
    'multi_order_count': 'mean',
    'total_order_count': 'mean',
    'gmv_total':'mean',
    'customer_segment': lambda x: x.value_counts().idxmax()
}).reset_index()
st.dataframe(cluster_summary, use_container_width=True)

st.markdown("""
**Observations:**
- Customers have been clustered into three distinct groups using KMeans: **Cluster 0 (red)**, **Cluster 1 (blue)**, and **Cluster 2 (green)**.
- All three clusters show a strong concentration in the **central zone**, particularly between **longitude 103.7–103.85** and **latitude 1.32–1.36**.
- **Cluster 2 (green)** appears more densely populated and widely spread, especially toward the **northwest quadrant**, suggesting broader spatial reach.
- **Cluster 0 (red)** tends to dominate the **eastern and southern extents**, while **Cluster 1 (blue)** is sparser and intermingled mostly within central areas.
- The segmentation confirms that **different customer groups are spatially interlaced**, but central urban zones remain the key overlap and hotspot.
""")