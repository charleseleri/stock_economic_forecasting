import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Load Data from SQLite Database
def load_data_from_sql(db_name="economic_forecast.db"):
    conn = sqlite3.connect(db_name)
    stock_df = pd.read_sql("SELECT * FROM Stock_Market", conn)
    gdp_df = pd.read_sql("SELECT * FROM GDP_Data", conn)
    inflation_df = pd.read_sql("SELECT * FROM Inflation_Data", conn)
    conn.close()
    return stock_df, gdp_df, inflation_df

# Function to Create a Dashboard
def create_dashboard():
    st.title("Stock Market & Economic Growth Forecasting Dashboard")

    # Load data
    stock_data, gdp_data, inflation_data = load_data_from_sql()

    # Convert date columns
    stock_data["Date"] = pd.to_datetime(stock_data["Date"])
    gdp_data["date"] = pd.to_datetime(gdp_data["date"])
    inflation_data["date"] = pd.to_datetime(inflation_data["date"])

    # Sidebar Filters
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", stock_data["Date"].min())
    end_date = st.sidebar.date_input("End Date", stock_data["Date"].max())

    # Filtered Data
    stock_filtered = stock_data[(stock_data["Date"] >= str(start_date)) & (stock_data["Date"] <= str(end_date))]
    gdp_filtered = gdp_data[(gdp_data["date"] >= str(start_date)) & (gdp_data["date"] <= str(end_date))]
    inflation_filtered = inflation_data[(inflation_data["date"] >= str(start_date)) & (inflation_data["date"] <= str(end_date))]

    # Stock Market Visualization
    st.subheader("S&P 500 Price Trend")
    fig1 = px.line(stock_filtered, x="Date", y="Closing Price", title="S&P 500 Closing Price Over Time")
    st.plotly_chart(fig1)

    # GDP Growth Visualization
    st.subheader("GDP Growth Over Time")
    fig2 = px.line(gdp_filtered, x="date", y="GDP", title="GDP Growth Trend")
    st.plotly_chart(fig2)

    # Inflation Trend Visualization
    st.subheader("Inflation Rate Over Time")
    fig3 = px.line(inflation_filtered, x="date", y="CPIAUCSL", title="Inflation Rate Trend")
    st.plotly_chart(fig3)

    # Summary Statistics
    st.sidebar.subheader("Summary Statistics")
    st.sidebar.write("S&P 500 Mean Price:", round(stock_filtered["Closing Price"].mean(), 2))
    st.sidebar.write("GDP Mean:", round(gdp_filtered["GDP"].mean(), 2))
    st.sidebar.write("Inflation Mean:", round(inflation_filtered["CPIAUCSL"].mean(), 2))

# Run the Dashboard
if __name__ == "__main__":
    create_dashboard()
