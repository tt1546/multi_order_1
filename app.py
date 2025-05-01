import streamlit as st

# Main App Title and Introduction
st.set_page_config(page_title="Multi-Order Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("Multi-Order Analysis Dashboard")

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
