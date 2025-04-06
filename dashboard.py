import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv("sales_data.csv")
df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])
df["Month"] = df["Sale_Date"].dt.to_period("M").astype(str)

# Title
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
regions = st.sidebar.multiselect("Select Region(s):", options=df["Region"].unique(), default=df["Region"].unique())
categories = st.sidebar.multiselect("Select Category(s):", options=df["Product_Category"].unique(), default=df["Product_Category"].unique())
sales_reps = st.sidebar.multiselect("Select Sales Rep(s):", options=df["Sales_Rep"].unique(), default=df["Sales_Rep"].unique())

# Apply filters
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Product_Category"].isin(categories)) &
    (df["Sales_Rep"].isin(sales_reps))
]

# KPIs
total_sales = filtered_df["Sales_Amount"].sum()
total_units = filtered_df["Quantity_Sold"].sum()
avg_discount = filtered_df["Discount"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"₹{total_sales:,.2f}")
col2.metric("📦 Total Units Sold", total_units)
col3.metric("🎁 Avg. Discount", f"{avg_discount:.2%}")

st.markdown("---")

# Monthly Revenue Chart
st.subheader("📈 Monthly Revenue Trend")
monthly_sales = filtered_df.groupby("Month")["Sales_Amount"].sum().sort_index()
st.line_chart(monthly_sales)

# Top Products by Revenue
st.subheader("🏆 Top 5 Products by Revenue")
top_products = filtered_df.groupby("Product_ID")["Sales_Amount"].sum().nlargest(5)
st.bar_chart(top_products)

# Sales by Region
st.subheader("🌍 Sales by Region")
region_sales = filtered_df.groupby("Region")["Sales_Amount"].sum()
fig, ax = plt.subplots()
region_sales.plot(kind="bar", color="skyblue", ax=ax)
ax.set_ylabel("Sales Amount")
ax.set_title("Sales by Region")
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Mayank Kumar | [Visit My Portfolio](https://thismayank1.github.io/Portfolio1/)")
