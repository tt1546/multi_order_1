import streamlit as st

# Main App Title and Introduction
st.set_page_config(page_title="Multi-Order Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("Multi-Order Analysis Dashboard")

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

st.markdown("""
This Streamlit app presents an interactive dashboard for multi-order analysis. 
Use the page navigation in the sidebar to explore:
- **Customer Segmentation**: Customer clusters and geographic distribution.
- **Multi-Order Analysis**: Patterns in multi-order behavior.
- **Temporal Pattern Exploration**: Yearly and time-series trends of multi-orders.
- **Fulfillment Cost Analysis**: Estimated cost savings from order consolidation.
- **Model Predictor**: Predict if an order will be a multi-order using the trained model.

<small><i>Note: A multi-order is defined as more than one order placed by the same customer_id within a 12-hour window.</i></small>
""", unsafe_allow_html=True)
