import requests
import pandas as pd
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Function to fetch stock market data (Yahoo Finance API)
def fetch_stock_data(ticker, interval="1d", range_period="1mo"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval={interval}&range={range_period}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        timestamps = data["chart"]["result"][0]["timestamp"]
        prices = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        
        # Convert timestamps to human-readable dates
        dates = pd.to_datetime(pd.Series(timestamps), unit='s')
        
        # Create DataFrame
        df = pd.DataFrame({"Date": dates, "Closing Price": prices})
        return df
    else:
        print("Failed to fetch stock data.")
        return None

# Function to fetch GDP and inflation data (FRED API - Federal Reserve)
def fetch_fred_data(series_id, api_key, start_date="2020-01-01"):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()["observations"]
        df = pd.DataFrame(data)
        df = df.rename(columns={"value": series_id})
        df["date"] = pd.to_datetime(df["date"])
        return df[["date", series_id]]
    else:
        print(f"Failed to fetch FRED data for {series_id}.")
        return None

# Function to scrape latest economic reports (IMF or Bloomberg via Selenium)
def scrape_economic_news():
    url = "https://www.bloomberg.com/markets/economics"
    
    options = Options()
    options.headless = True
    service = Service("/path/to/chromedriver")  # Adjust path for local setup
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    headlines = soup.find_all("h3", class_="story-package-module__headline")
    news = [headline.text.strip() for headline in headlines[:5]]
    
    return news

# Store data in SQLite
def store_data_in_sqlite(stock_df, gdp_df, inflation_df, db_name="economic_forecast.db"):
    conn = sqlite3.connect(db_name)
    stock_df.to_sql("Stock_Market", conn, if_exists="replace", index=False)
    gdp_df.to_sql("GDP_Data", conn, if_exists="replace", index=False)
    inflation_df.to_sql("Inflation_Data", conn, if_exists="replace", index=False)
    conn.close()

# Run data collection
if __name__ == "__main__":
    stock_ticker = "SPY"  # S&P 500 ETF
    fred_api_key = "YOUR_FRED_API_KEY"  # Replace with your API key
    
    # Fetch data
    stock_data = fetch_stock_data(stock_ticker)
    gdp_data = fetch_fred_data("GDP", fred_api_key)
    inflation_data = fetch_fred_data("CPIAUCSL", fred_api_key)
    news_headlines = scrape_economic_news()
    
    # Store in SQL database
    if stock_data is not None and gdp_data is not None and inflation_data is not None:
        store_data_in_sqlite(stock_data, gdp_data, inflation_data)
    
    # Print latest economic news
    print("Latest Economic News:")
    for news in news_headlines:
        print("-", news)
