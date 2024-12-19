import pandas as pd
import matplotlib.pyplot as plt

# Load forecasted data
dxy_forecast = pd.read_csv("processed_data/DXY_Forecast.csv")
nifty_forecast = pd.read_csv("processed_data/Nifty_Forecast.csv")

# Normalize the date columns by removing the time part
dxy_forecast['ds'] = pd.to_datetime(dxy_forecast['ds']).dt.date
nifty_forecast['ds'] = pd.to_datetime(nifty_forecast['ds']).dt.date

# Merge data on normalized dates
merged_forecast = pd.merge(
    dxy_forecast[['ds', 'yhat']],
    nifty_forecast[['ds', 'yhat']],
    on='ds',
    how='inner',  # Include only matching dates
    suffixes=('_DXY', '_Nifty')
)

# Rename columns for clarity
merged_forecast.columns = ['Date', 'DXY_Forecast', 'Nifty_Forecast']

# Normalize forecasted values for better comparison
merged_forecast['DXY_Normalized'] = (
    (merged_forecast['DXY_Forecast'] - merged_forecast['DXY_Forecast'].min()) /
    (merged_forecast['DXY_Forecast'].max() - merged_forecast['DXY_Forecast'].min())
)
merged_forecast['Nifty_Normalized'] = (
    (merged_forecast['Nifty_Forecast'] - merged_forecast['Nifty_Forecast'].min()) /
    (merged_forecast['Nifty_Forecast'].max() - merged_forecast['Nifty_Forecast'].min())
)

# Check merged and normalized data
print("Merged and Normalized Forecast Head:")
print(merged_forecast)

# Plot normalized trends
plt.figure(figsize=(12, 6))
plt.plot(merged_forecast['Date'], merged_forecast['DXY_Normalized'], label="DXY (Normalized)", color='blue')
plt.plot(merged_forecast['Date'], merged_forecast['Nifty_Normalized'], label="Nifty 50 (Normalized)", color='orange')
plt.title("Comparison of Forecasted Trends: DXY vs. Nifty 50 (Normalized)")
plt.xlabel("Date")
plt.ylabel("Normalized Values")
plt.legend()
plt.grid()
plt.show()

# Calculate correlation between forecasted values
correlation = merged_forecast['DXY_Forecast'].corr(merged_forecast['Nifty_Forecast'])
print(f"Correlation between DXY and Nifty forecasted values: {correlation:.2f}")
