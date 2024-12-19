import pandas as pd

# Load DXY forecast data
dxy_forecast = pd.read_csv("processed_data/DXY_Forecast.csv")
print("DXY Forecast Head:")
print(dxy_forecast.head())

# Load Nifty forecast data
nifty_forecast = pd.read_csv("processed_data/Nifty_Forecast.csv")
print("\nNifty Forecast Head:")
print(nifty_forecast.head())
