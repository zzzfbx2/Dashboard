import yfinance as yf
import pandas as pd

# Define the assets to fetch data for
assets = {
    "Dollar Index (DXY)": "DX-Y.NYB",
    "Nifty 50": "^NSEI",
    "Nasdaq": "^IXIC",
    "S&P 500": "^GSPC",
    "USD/INR": "USDINR=X",
    "Gold": "GC=F",
    "Crude Oil": "CL=F"
}

# Timeframe for data collection
time_period = "1y"  # Last 1 year
interval = "1d"  # Daily data

# Create a folder for storing the data
output_folder = "historical_data"
import os
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Fetch and save data
for asset_name, ticker in assets.items():
    print(f"Fetching data for {asset_name} ({ticker})...")
    try:
        data = yf.Ticker(ticker).history(period=time_period, interval=interval)
        if not data.empty:
            # Save to CSV
            output_path = f"{output_folder}/{asset_name.replace(' ', '_')}.csv"
            data.to_csv(output_path)
            print(f"Saved {asset_name} data to {output_path}")
        else:
            print(f"No data found for {asset_name}")
    except Exception as e:
        print(f"Error fetching data for {asset_name}: {e}")

print("Data collection complete!")
