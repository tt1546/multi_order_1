import streamlit as st
import pandas as pd
import xgboost as xgb
import plotly.express as px

st.set_page_config(page_title="Multi-Order Predictor", layout="wide")
st.title("Multi-Order Predictor")
st.divider()

# ---------------------------- #
# Section: Prediction Interface
# ---------------------------- #
st.subheader("Prediction Interface")
st.write("Input the order/customer features below to predict the probability that an order will be a **multi-order**.")

# Input fields
option_id_list = [f"Option_{i}" for i in range(24)]
option_id_input = st.selectbox("Option ID", options=option_id_list, index=0)
amount = st.number_input("Amount (¥)", min_value=0.0, value=100.0)
quantity = st.number_input("Quantity", min_value=1, value=1)
label_price = st.number_input("Label Price (¥)", min_value=0.0, value=100.0)
discount = st.number_input("Discount (0–1)", min_value=0.0, max_value=1.0, value=0.0)
order_weekday = st.selectbox("Order Weekday", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=0)
order_hour = st.slider("Order Hour", min_value=0, max_value=23, value=12)
is_weekend = st.checkbox("Is Weekend?", value=False)
is_night = st.checkbox("Is Night?", value=False)
cluster_id = st.selectbox("Customer Cluster", [0, 1, 2], index=0)
member_level = st.selectbox("Member Level", ["A", "B", "C"], index=2)
customer_segment = st.selectbox("Customer Segment", ["Low", "Medium", "High", "Very High"], index=2)
customer_group = st.selectbox("Customer Group ID", ["CustomerGroup_0", "CustomerGroup_1", "CustomerGroup_2"], index=0)

# Encode inputs
weekday_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
member_map = {"A": 0, "B": 1, "C": 2}
segment_map = {"Low": 0, "Medium": 1, "High": 2, "Very High": 3}

order_weekday_num = weekday_map.get(order_weekday, 0)
is_weekend_num = int(is_weekend)
is_night_num = int(is_night)
member_level_num = member_map.get(member_level, 0)
customer_segment_num = segment_map.get(customer_segment, 0)

try:
    customer_group_num = int(customer_group.split('_')[-1])
except:
    customer_group_num = 0

try:
    option_num = int(option_id_input.split('_')[-1])
except:
    option_num = 0

input_features = pd.DataFrame([{
    "quantity": quantity,
    "label_price": label_price,
    "discount": discount,
    "amount": amount,
    "order_weekday": order_weekday_num,
    "order_hour": order_hour,
    "is_weekend": is_weekend_num,
    "is_night": is_night_num,
    "cluster": cluster_id,
    "member_level": member_level_num,
    "customer_segment": customer_segment_num,
    "customer_group_id": customer_group_num,
    "option_id": option_num
}])

# Cached model loader
@st.cache_resource
def load_model():
    model = xgb.Booster()
    model.load_model("models/xgb_model.json")
    return model

model = load_model()

# Predict
if st.button("Predict"):
    dmatrix = xgb.DMatrix(input_features)
    y_prob = model.predict(dmatrix)[0]
    y_pred = int(y_prob >= 0.5)

    st.write(f"**Predicted Probability of Multi-Order:** {y_prob*100:.2f}% ({'Yes' if y_pred == 1 else 'No'} likelihood)")
    if y_pred == 1:
        st.success("The model predicts this order is likely to be a multi-order.")
    else:
        st.info("The model predicts this order is not likely to be a multi-order.")
# ---------------------------- #
# Section: Feature Importance
# ---------------------------- #
st.subheader("Feature Importance Analysis")

st.markdown("""
**Purpose:**  
To understand which features contribute most to the model's decisions and interpret predictive behavior.
""")

booster = model.get_booster()
importance = booster.get_score(importance_type='weight')

importance_df = pd.DataFrame({
    'feature': list(importance.keys()),
    'importance': list(importance.values())
}).sort_values(by='importance', ascending=False)

# Plotly bar chart
fig_imp = px.bar(
    importance_df,
    x='importance',
    y='feature',
    orientation='h',
    title="Feature Importance (by weight)",
    labels={'importance': 'Importance Score', 'feature': 'Feature'},
    color_discrete_sequence=['skyblue']
)
fig_imp.update_layout(
    plot_bgcolor='white',
    yaxis=dict(categoryorder='total ascending')
)

st.plotly_chart(fig_imp, use_container_width=True)

st.markdown("""
**Observations:**

- **Discount** and **Amount** are the most influential features, indicating that pricing-related factors are highly predictive of multi-order behavior.
- **Order Hour** and **Order Weekday** also rank highly, suggesting a strong temporal pattern in customer multi-order activity.
- **Option ID** and **Customer Group ID** contribute meaningfully, likely capturing product-type or campaign-specific behavior.
- Features like **Cluster**, **Is Night**, and **Is Weekend** show relatively low importance, implying that spatial and time-of-day aspects may have limited standalone predictive power.
""")
