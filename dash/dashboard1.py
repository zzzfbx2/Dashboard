import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import urllib.parse  # For URL encoding
import pandas as pd
import matplotlib.pyplot as plt

# Set up the Streamlit page layout
st.set_page_config(page_title="Trading Dashboard", layout="wide")

# Function to fetch news from Google RSS Feeds
def fetch_rss_news(query):
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        feed = feedparser.parse(rss_url)
        articles = feed.entries[:5]  # Get top 5 articles
        return articles
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

# Function to fetch and plot data
def fetch_data(ticker, name, period):
    try:
        # Adjust interval for short timeframes
        interval = "5m" if period == "1d" else "1d"
        data = yf.Ticker(ticker).history(period=period, interval=interval)
        
        # Handle missing data
        if data.empty:
            st.warning(f"No data available for {name} in the selected timeframe ({period}).")
            return None, None
        
        # Extract latest value
        latest_value = data["Close"].iloc[-1]
        
        # Create the chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name=name))
        fig.update_layout(title=f"{name} - {period} Chart", xaxis_title="Time", yaxis_title="Price")
        return fig, latest_value
    except Exception as e:
        st.error(f"Error fetching data for {name}: {e}")
        return None, None

# Function to generate AI insights based on Dollar Index value
def generate_ai_insights(dxy_value):
    insights = []
    if dxy_value > 105:
        insights.append("🟢 The Dollar Index is above 105, signaling a stronger USD.")
        insights.append("- Emerging markets like India may face capital outflows.")
        insights.append("- Gold prices may come under pressure due to a stronger USD.")
        insights.append("- Crude oil prices could soften as a stronger USD increases costs for importers.")
        insights.append("- Consider monitoring USD/INR for further appreciation in the dollar.")
    else:
        insights.append("🟡 The Dollar Index is below 105, indicating a stable USD.")
        insights.append("- Emerging markets could benefit from stable inflows.")
        insights.append("- Commodities like gold and crude oil may remain range-bound.")
    return insights

# Load forecasted data
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

# Dashboard Title
st.title("📊 Enhanced Trading Dashboard")

# Sidebar for user inputs
st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (in seconds)", 5, 60, 30)
timeframe = st.sidebar.selectbox(
    "Timeframe",
    options=["1d", "5d", "1mo", "3mo", "6mo", "1y"],
    index=0
)

# Sidebar for single-index selection
st.sidebar.header("View Single Index")
selected_index = st.sidebar.selectbox(
    "Choose an Index to Display:",
    options={
        "Dollar Index (DXY)": "DX-Y.NYB",
        "Nifty 50": "^NSEI",
        "Nasdaq": "^IXIC",
        "Dow Jones (DJI)": "^DJI",
        "S&P 500": "^GSPC",
        "FTSE 100": "^FTSE",
        "Nikkei 225": "^N225"
    }
)

# Define tickers for all indices
ticker_mapping = {
    "Dollar Index (DXY)": "DX-Y.NYB",
    "Nifty 50": "^NSEI",
    "Nasdaq": "^IXIC",
    "Dow Jones (DJI)": "^DJI",
    "S&P 500": "^GSPC",
    "FTSE 100": "^FTSE",
    "Nikkei 225": "^N225"
}

# Display all indices in the overview section
st.header("Overview of All Indices")
all_indices = [
    "Dollar Index (DXY)",
    "Nifty 50",
    "Nasdaq",
    "Dow Jones (DJI)",
    "S&P 500",
    "FTSE 100",
    "Nikkei 225",
]

# Initialize Dollar Index value
dxy_value = None

# Organize indices into rows of three columns
for i in range(0, len(all_indices), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(all_indices):
            index_name = all_indices[i + j]
            col.subheader(index_name)
            chart, latest_value = fetch_data(ticker_mapping[index_name], index_name, timeframe)
            if chart:
                col.plotly_chart(chart, use_container_width=True, key=f"chart_{index_name}")
            # Capture Dollar Index value for AI insights
            if index_name == "Dollar Index (DXY)":
                dxy_value = latest_value

# AI Insights Section
if dxy_value is not None:
    st.header("🤖 AI Insights")
    insights = generate_ai_insights(dxy_value)
    for insight in insights:
        st.write(insight)

# Forecast Comparison Section
st.header("🔗 Forecast Comparison")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(merged_forecast['Date'], merged_forecast['DXY_Normalized'], label="DXY (Normalized)", color='blue')
ax.plot(merged_forecast['Date'], merged_forecast['Nifty_Normalized'], label="Nifty 50 (Normalized)", color='orange')
ax.set_title("Comparison of Forecasted Trends: DXY vs. Nifty 50 (Normalized)")
ax.set_xlabel("Date")
ax.set_ylabel("Normalized Values")
ax.legend()
st.pyplot(fig)

# News Section
st.header("🌍 Global Market News")
news_articles = fetch_rss_news("Dollar Index OR global economy")
if news_articles:
    for article in news_articles:
        st.write(f"### [{article.title}]({article.link})")
        st.write(f"Published At: {article.published}")
        st.write(article.summary)
        st.write("---")

# Sidebar: Single-index view
st.sidebar.header("View Selected Index")
if selected_index:
    st.sidebar.subheader(selected_index)
    single_chart, _ = fetch_data(ticker_mapping[selected_index], selected_index, timeframe)
    if single_chart:
        st.sidebar.plotly_chart(single_chart, use_container_width=True, key="single_chart")

# Footer
st.write("💡 Refresh rate set to:", refresh_rate, "seconds. Dashboard updates automatically.")
st.write("Data fetched using Yahoo Finance and Google News RSS feeds.")
