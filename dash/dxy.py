import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Load processed data for Dollar Index
file_path = "processed_data/Dollar_Index_(DXY)_Processed.csv"
data = pd.read_csv(file_path)

# Preprocess data for Prophet
data['Date'] = pd.to_datetime(data['Date'], utc=True).dt.tz_localize(None)  # Ensure timezone-naive datetime
data = data[['Date', 'Close']]  # Select only Date and Close columns
data.columns = ['ds', 'y']  # Rename columns for Prophet compatibility

# Initialize Prophet model
model = Prophet()
model.fit(data)

# Create a dataframe for future dates (7 days)
future = model.make_future_dataframe(periods=7)  # Predict next 7 days
forecast = model.predict(future)

# Plot forecast
fig1 = model.plot(forecast)
plt.title("Dollar Index (DXY) - Forecast for Next 7 Days")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

# Plot components (trend and seasonality)
fig2 = model.plot_components(forecast)
plt.show()

# Save forecast to CSV
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(
    "processed_data/DXY_Forecast.csv", index=False
)
print("Forecast saved to 'processed_data/DXY_Forecast.csv'")
