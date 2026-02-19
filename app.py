import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Online Food Delivery Analysis", layout="wide")
st.title("🍔 Online Food Delivery Analysis Dashboard")

# ---------------- DATABASE CONNECTION ----------------
password = quote_plus("Nithik@20")  # change if needed

engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost:3306/food_delivery_db"
)

df = pd.read_sql("SELECT * FROM orders", engine)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    df["city"].unique(),
    default=df["city"].unique()
)

cuisine_filter = st.sidebar.multiselect(
    "Select Cuisine",
    df["cuisine_type"].unique(),
    default=df["cuisine_type"].unique()
)

day_filter = st.sidebar.multiselect(
    "Select Day Type",
    df["day_type"].unique(),
    default=df["day_type"].unique()
)

df = df[
    (df["city"].isin(city_filter)) &
    (df["cuisine_type"].isin(cuisine_filter)) &
    (df["day_type"].isin(day_filter))
]

# ---------------- KPI SECTION ----------------
total_orders = len(df)
total_revenue = df["order_value"].sum()
avg_order_value = df["order_value"].mean()
avg_delivery_time = df["delivery_time_min"].mean()
avg_profit_margin = df["profit_margin"].mean()

if total_orders > 0:
    cancellation_rate = (
        (df["order_status"] == "Cancelled").sum() / total_orders
    ) * 100
else:
    cancellation_rate = 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("Total Revenue", f"₹ {total_revenue:,.2f}")
col3.metric("Avg Order Value", f"₹ {avg_order_value:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Avg Delivery Time (mins)", f"{avg_delivery_time:.2f}")
col5.metric("Cancellation Rate (%)", f"{cancellation_rate:.2f}")
col6.metric("Avg Profit Margin", f"{avg_profit_margin:.2f}")

st.divider()

# =========================
# CUSTOMER ANALYSIS
# =========================
st.header("👥 Customer Analysis")

st.subheader("Top 10 Spending Customers")
top_customers = df.groupby("customer_id")["order_value"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_customers)

st.subheader("Age Group vs Average Order Value")
age_analysis = df.groupby("age_group")["order_value"].mean()
st.bar_chart(age_analysis)

# =========================
# REVENUE & PROFIT ANALYSIS
# =========================
st.header("💰 Revenue & Profit Analysis")

st.subheader("Monthly Revenue Trend")
monthly_revenue = df.groupby("order_month")["order_value"].sum()
st.line_chart(monthly_revenue)

st.subheader("City-wise Revenue")
city_revenue = df.groupby("city")["order_value"].sum()
st.bar_chart(city_revenue)

st.subheader("Cuisine-wise Revenue")
cuisine_revenue = df.groupby("cuisine_type")["order_value"].sum()
st.bar_chart(cuisine_revenue)

st.subheader("Discount vs Profit Margin")
discount_profit = df.groupby("discount_applied")["profit_margin"].mean()
st.line_chart(discount_profit)

# =========================
# DELIVERY PERFORMANCE
# =========================
st.header("🚚 Delivery Performance")

st.subheader("Average Delivery Time by City")
delivery_city = df.groupby("city")["delivery_time_min"].mean()
st.bar_chart(delivery_city)

st.subheader("Delivery Rating vs Delivery Time")
rating_time = df.groupby("delivery_time_min")["delivery_rating"].mean()
st.line_chart(rating_time)

st.subheader("Distance vs Delivery Time")
distance_time = df.groupby("distance_km")["delivery_time_min"].mean()
st.line_chart(distance_time)

# =========================
# RESTAURANT PERFORMANCE
# =========================
st.header("🏪 Restaurant Performance")

st.subheader("Top 10 Rated Restaurants")
top_restaurants = df.groupby("restaurant_name")["restaurant_rating"].mean().sort_values(ascending=False).head(10)
st.bar_chart(top_restaurants)

st.subheader("Cuisine-wise Average Rating")
cuisine_rating = df.groupby("cuisine_type")["restaurant_rating"].mean()
st.bar_chart(cuisine_rating)

# =========================
# OPERATIONAL INSIGHTS
# =========================
st.header("⚙ Operational Insights")

st.subheader("Peak Hour Demand")
peak_hour = df["peak_hour"].value_counts()
st.bar_chart(peak_hour)

st.subheader("Payment Mode Distribution")
payment_mode = df["payment_mode"].value_counts()
st.bar_chart(payment_mode)

st.subheader("Cancellation Reason Analysis")
cancel_reason = df[df["order_status"] == "Cancelled"]["cancellation_reason"].value_counts()
st.bar_chart(cancel_reason)

st.success("✅ Full Project Dashboard Completed Successfully!")
