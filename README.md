# Stock Market & Economic Growth Forecasting

## Overview
This project forecasts **stock market trends, GDP growth, and inflation rates** using **machine learning models (ARIMA, Monte Carlo Simulation, XGBoost)** and real-time economic data from **Yahoo Finance, FRED API, and Bloomberg (via Selenium scraping).**

## Features
- **Fetches real-time stock market & economic data** via API & web scraping.
- **Stores data in SQLite for structured analysis.**
- **Forecasts stock prices, GDP growth, and inflation trends.**
- **Generates an interactive visualization dashboard using Streamlit.**
- **Uses ARIMA & Monte Carlo simulation for financial forecasting.**

## Project Structure
```
Stock_Economic_Forecasting/
│-- README.md                 # Project Overview & Instructions
│-- data_collection.py        # Fetches stock, GDP, and inflation data
│-- forecasting_model.py      # Runs ARIMA & ML-based predictions
│-- database.sql              # Stores historical data in SQLite
│-- dashboard.py              # Generates interactive charts & visuals
│-- requirements.txt          # Dependencies for setup
```

## Installation & Setup
### 1️⃣ Install Dependencies
Run the following command to install required Python libraries:
```
pip install -r requirements.txt
```

### 2️⃣ Run the Data Collection Script
```
python data_collection.py
```
This will fetch stock market data, GDP, and inflation rates and store them in SQLite.

### 3️⃣ Run the Forecasting Model
```
python forecasting_model.py
```
This will generate forecasts for stock prices, GDP growth, and inflation.

### 4️⃣ Run the Interactive Dashboard
```
streamlit run dashboard.py
```
This will launch a web-based visualization for interacting with data.

## Technologies Used
- **Python** (Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit)
- **APIs** (Yahoo Finance, FRED - Federal Reserve)
- **Machine Learning** (ARIMA, Monte Carlo, XGBoost)
- **SQL Database** (SQLite for data storage)
- **Web Scraping** (Selenium & BeautifulSoup for economic news)

## Author
**Charles Eleri**

## Next Steps
- Enhance ML models with **deep learning (LSTM for time-series)**.
- Expand API support for **crypto market & forex forecasting**.
- Deploy the dashboard to **AWS or Heroku** for public access.

---
🔹 **GitHub Repo:** [github.com/charleseleri](https://github.com/charleseleri)