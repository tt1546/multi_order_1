# Multi-Order Streamlit Dashboard

This project is a Streamlit-based interactive dashboard for analyzing multi-order customer behavior in a delivery/logistics context. The dashboard helps visualize trends, cluster customers, predict multi-order likelihood, and evaluate fulfillment cost savings from order merging.

## Project Structure

```
├── app.py                       # Main entry point
├── pages/
│   ├── 1_Customer_Clustering.py
│   ├── 2_Multi_Order_Analysis.py
│   ├── 3_Temporal_Pattern_Exploration.py
│   ├── 4_Fulfillment_Cost_Analysis.py
│   └── 5_Model_Predictor.py
├── models/
│   └── xgb_model.json           # Pre-trained XGBoost model
├── data/                        # CSV data files
├── requirements.txt
└── README.md
```

## Features

### 1. Customer Clustering
- View multi-order ratio distributions
- Explore GMV and repeat behavior segments
- Visualize customer spatial clusters using KMeans

### 2. Multi-Order Analysis
- Analyze which options (products/services) tend to be ordered repeatedly
- Identify cluster-specific purchase preferences

### 3. Temporal Pattern Exploration
- Hourly, weekly, and daily trends of multi-orders
- Reveal time-based behavioral patterns

### 4. Fulfillment Cost Analysis
- Estimate cost savings from merged multi-order shipments
- Visualize savings by cluster

### 5. Multi-Order Predictor
- Input order features and receive prediction from a pre-trained XGBoost model
- See feature importance analysis

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/multi-order-dashboard.git
cd multi-order-dashboard
```

### 2. Install dependencies

Make sure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

## Data Files

Place all required CSVs in the `data/` directory. Key files include:

- cluster_simulation_df.csv
- multi_order_stats.csv
- segment_distribution.csv
- hourly_stats.csv
- weekly_stats.csv
- annual_stats.csv
- customer_profile.csv
- hotzone_customers.csv
- option_comparison.csv
- top_option_per_cluster.csv
- etc.

## Model

The predictor loads a pretrained XGBoost model from:

```
models/xgb_model.json
```

Make sure this file is present in the correct path.

## Authors

Built by Group 13  
For academic/educational purposes only.