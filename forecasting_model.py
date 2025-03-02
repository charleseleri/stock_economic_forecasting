import pandas as pd
import numpy as np
import sqlite3
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data from SQLite Database
def load_data_from_sql(db_name="economic_forecast.db"):
    conn = sqlite3.connect(db_name)
    stock_df = pd.read_sql("SELECT * FROM Stock_Market", conn)
    gdp_df = pd.read_sql("SELECT * FROM GDP_Data", conn)
    inflation_df = pd.read_sql("SELECT * FROM Inflation_Data", conn)
    conn.close()
    
    return stock_df, gdp_df, inflation_df

# Function to Train ARIMA Model for Forecasting
def train_arima_model(data, column, order=(2,1,2), steps=12):
    data["Date"] = pd.to_datetime(data["Date"])
    data.set_index("Date", inplace=True)
    
    model = ARIMA(data[column], order=order)
    model_fit = model.fit()
    
    forecast = model_fit.forecast(steps=steps)
    return model_fit, forecast

# Function to Plot Forecasting Results
def plot_forecast(original_data, forecast, title, ylabel):
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=original_data.index, y=original_data, label="Historical Data", color="blue")
    sns.lineplot(x=pd.date_range(start=original_data.index[-1], periods=len(forecast), freq="M"), 
                 y=forecast, label="Forecast", color="red", linestyle="dashed")
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Run Forecasting Models
if __name__ == "__main__":
    stock_data, gdp_data, inflation_data = load_data_from_sql()
    
    # Train ARIMA Model for S&P 500 Stock Prices
    sp500_model, sp500_forecast = train_arima_model(stock_data, "Closing Price")
    plot_forecast(stock_data["Closing Price"], sp500_forecast, "S&P 500 Price Forecast", "Stock Price ($)")
    
    # Train ARIMA Model for GDP Growth
    gdp_model, gdp_forecast = train_arima_model(gdp_data, "GDP")
    plot_forecast(gdp_data["GDP"], gdp_forecast, "GDP Growth Forecast", "GDP ($B)")
    
    # Train ARIMA Model for Inflation Rate
    inflation_model, inflation_forecast = train_arima_model(inflation_data, "CPIAUCSL")
    plot_forecast(inflation_data["CPIAUCSL"], inflation_forecast, "Inflation Rate Forecast", "CPI Index")
