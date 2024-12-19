import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set up Streamlit page
st.set_page_config(page_title="Trading Dashboard", layout="wide")
st.title("📊 Enhanced Trading Dashboard")

# Load processed and forecasted data
dxy_forecast = pd.read_csv("processed_data/DXY_Forecast.csv")
nifty_forecast = pd.read_csv("processed_data/Nifty_Forecast.csv")

# Normalize the date columns
dxy_forecast['ds'] = pd.to_datetime(dxy_forecast['ds']).dt.date
nifty_forecast['ds'] = pd.to_datetime(nifty_forecast['ds']).dt.date

# Merge forecasted data for comparison
merged_forecast = pd.merge(
    dxy_forecast[['ds', 'yhat']],
    nifty_forecast[['ds', 'yhat']],
    on='ds',
    how='inner',
    suffixes=('_DXY', '_Nifty')
)
merged_forecast.columns = ['Date', 'DXY_Forecast', 'Nifty_Forecast']

# Normalize forecasted values
merged_forecast['DXY_Normalized'] = (
    (merged_forecast['DXY_Forecast'] - merged_forecast['DXY_Forecast'].min()) /
    (merged_forecast['DXY_Forecast'].max() - merged_forecast['DXY_Forecast'].min())
)
merged_forecast['Nifty_Normalized'] = (
    (merged_forecast['Nifty_Forecast'] - merged_forecast['Nifty_Forecast'].min()) /
    (merged_forecast['Nifty_Forecast'].max() - merged_forecast['Nifty_Forecast'].min())
)

# Sidebar for navigation
st.sidebar.header("Dashboard Navigation")
section = st.sidebar.radio("Go to Section:", ["Overview", "Forecasts", "Comparison & Correlation"])

if section == "Overview":
    st.subheader("📈 Overview of Data")
    st.write("This dashboard provides forecasts and insights for the Dollar Index (DXY) and Nifty 50.")

elif section == "Forecasts":
    st.subheader("🔮 Individual Forecasts")
    st.write("### Dollar Index (DXY) Forecast")
    st.line_chart(dxy_forecast.set_index('ds')['yhat'])

    st.write("### Nifty 50 Forecast")
    st.line_chart(nifty_forecast.set_index('ds')['yhat'])

elif section == "Comparison & Correlation":
    st.subheader("🔗 Comparison of DXY and Nifty 50 Forecasts")
    
    # Plot normalized trends
    st.write("### Normalized Forecast Trends")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(merged_forecast['Date'], merged_forecast['DXY_Normalized'], label="DXY (Normalized)", color='blue')
    ax.plot(merged_forecast['Date'], merged_forecast['Nifty_Normalized'], label="Nifty 50 (Normalized)", color='orange')
    ax.set_title("Comparison of Forecasted Trends: DXY vs. Nifty 50 (Normalized)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Values")
    ax.legend()
    st.pyplot(fig)

    # Correlation Insights
    st.write("### Correlation Insights")
    correlation = merged_forecast['DXY_Forecast'].corr(merged_forecast['Nifty_Forecast'])
    st.write(f"The correlation coefficient between DXY and Nifty forecasts is **{correlation:.2f}**.")
    if correlation < -0.5:
        st.write("🟢 A significant inverse relationship exists between DXY and Nifty.")
    elif correlation > 0.5:
        st.write("🟢 A significant positive relationship exists between DXY and Nifty.")
    else:
        st.write("🟠 The relationship between DXY and Nifty is weak or inconsistent.")

# Footer
st.sidebar.write("---")
st.sidebar.write("Created with ❤️ by Raj")
