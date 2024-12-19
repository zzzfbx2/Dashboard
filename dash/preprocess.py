import pandas as pd
import matplotlib.pyplot as plt
import os

# Create a folder for processed data
output_folder = "processed_data"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to preprocess data
def preprocess_data(file_path, asset_name):
    print(f"Processing data for {asset_name}...")

    # Load data
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found!")
        return None

    # Check for missing values
    print(f"Missing values before preprocessing:\n{data.isnull().sum()}")

    # Fill missing values
    data.fillna(method='ffill', inplace=True)

    # Convert Date column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Set Date as the index
    data.set_index('Date', inplace=True)

    # Add daily percentage change
    data['Daily_Change_%'] = data['Close'].pct_change() * 100

    # Add moving averages
    data['7_Day_MA'] = data['Close'].rolling(window=7).mean()
    data['30_Day_MA'] = data['Close'].rolling(window=30).mean()

    # Add volatility (7-day rolling standard deviation)
    data['Volatility'] = data['Close'].rolling(window=7).std()

    # Save processed data
    output_path = f"{output_folder}/{asset_name}_Processed.csv"
    data.to_csv(output_path)
    print(f"Processed data saved to {output_path}\n")
    return data

# Preprocess Dollar Index (DXY)
dxy_file_path = "historical_data/Dollar_Index_(DXY).csv"
dxy_data = preprocess_data(dxy_file_path, "Dollar_Index_(DXY)")

# Preprocess Nifty 50
nifty_file_path = "historical_data/Nifty_50.csv"
nifty_data = preprocess_data(nifty_file_path, "Nifty_50")

# Visualize Dollar Index Data
if dxy_data is not None:
    plt.figure(figsize=(12, 6))
    plt.plot(dxy_data.index, dxy_data['Close'], label='Close Price', color='blue')
    plt.plot(dxy_data.index, dxy_data['7_Day_MA'], label='7-Day MA', color='orange')
    plt.plot(dxy_data.index, dxy_data['30_Day_MA'], label='30-Day MA', color='green')
    plt.title("Dollar Index (DXY) - Price and Moving Averages")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(dxy_data.index, dxy_data['Volatility'], label='Volatility', color='red')
    plt.title("Dollar Index (DXY) - Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.show()

# Visualize Nifty 50 Data
if nifty_data is not None:
    plt.figure(figsize=(12, 6))
    plt.plot(nifty_data.index, nifty_data['Close'], label='Close Price', color='blue')
    plt.plot(nifty_data.index, nifty_data['7_Day_MA'], label='7-Day MA', color='orange')
    plt.plot(nifty_data.index, nifty_data['30_Day_MA'], label='30-Day MA', color='green')
    plt.title("Nifty 50 - Price and Moving Averages")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(nifty_data.index, nifty_data['Volatility'], label='Volatility', color='red')
    plt.title("Nifty 50 - Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.show()
