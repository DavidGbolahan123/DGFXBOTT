import streamlit as st
import streamlit_autorefresh as st_autorefresh
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import numpy as np
import datetime
import os
import config
import plotly.graph_objects as go
from newsapi import NewsApiClient
from transformers import pipeline
import matplotlib.pyplot as plt

# Add this early in your script
st_autorefresh(interval=60 * 1000, key="dashboard_autorefresh")  # refresh every 60 secs

csv_path = config.SIGNAL_LOG_CSV_PATH

st.set_page_config(page_title="DGFXBot Dashboard", layout="wide")

st.title("📊 DGFXBot Signal Dashboard")

csv_path = config.SIGNAL_LOG_CSV_PATH
symbols = config.MONITORED_PAIRS  # Or whatever variable name you use in config.py

# Load signal log if it exists
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)

    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])

    # Keep only the most recent signal for each symbol

if 'time' in df.columns:
    df['time'] = pd.to_datetime(df['time'])
    latest_signals = df.sort_values("time").groupby("symbol").tail(1)
else:
    latest_signals = df.copy()

# Layout: 4 cards per row
cols = st.columns(4)

# Display each currency pair from config, even if no signal yet
for idx, symbol in enumerate(symbols):
    col = cols[idx % 4]
    with col:
        st.markdown(f"### {symbol}")

        # Filter for this symbol
        symbol_data = latest_signals[latest_signals["symbol"] == symbol]

        if not symbol_data.empty:
            row = symbol_data.iloc[0]

            signal = row.get("signal", "Unknown")
            strength = row.get("strength", "N/A")
            ai_score = row.get("ai_score", "N/A")
            time = row.get("time", "Unknown")

            if isinstance(time, pd.Timestamp):
                time = time.strftime("%Y-%m-%d %H:%M:%S")

            st.success(f"🟢 Signal: **{signal.upper()}**")
            st.write(f"📈 Strength: `{strength}`")
            st.write(f"🤖 AI Score: `{ai_score}`")
            st.write(f"🕒 Time: `{time}`")
        else:
            st.warning("⚠️ No signal yet")
            st.caption("🔄 Waiting for new analysis...")

# Optional: show recent logs (last 10)
st.divider()
st.subheader("🧾 Recent Signal Logs")

if not df.empty:
    st.dataframe(df.sort_values("time", ascending=False).head(10), use_container_width=True)
else:
    st.info("No signal log data found.")

# === ENHANCEMENT START ===

import time

# Sidebar navigation
st.sidebar.title("📂 DGFXBot Navigation")
page = st.sidebar.radio("Sections", [
    "📊 Signal Dashboard",
    "📉 Technical Analysis",
    "💬 Market Sentiment",
    "🔁 Backtesting",
    "📈 Performance Overview"
])

st.sidebar.markdown("---")
st.sidebar.caption("⚙️ Auto-refresh every 60 seconds")


# Placeholder strength scoring logic
def compute_signal_strength(row):
    """Compute signal strength out of 100 based on indicators (mock logic)"""
    strength_score = 0

    # Mock: Add fixed points if signal has certain indicators active (could be booleans or signals from backend)
    if "rsi" in row and row["rsi"] != "N/A":
        strength_score += 15
    if "macd" in row and row["macd"] != "N/A":
        strength_score += 15
    if "ema" in row and row["ema"] != "N/A":
        strength_score += 15
    if "fibonacci" in row and row["fibonacci"] != "N/A":
        strength_score += 15
    if "support_resistance" in row and row["support_resistance"] != "N/A":
        strength_score += 20
    if "smc" in row and row["smc"] != "N/A":
        strength_score += 20

    return f"{strength_score}/100"

# Enhance signal strength display with actual % score
for idx, symbol in enumerate(symbols):
    col = cols[idx % 4]
    with col:
        st.markdown(f"### {symbol}")

        symbol_data = latest_signals[latest_signals["symbol"] == symbol]
        if not symbol_data.empty:
            row = symbol_data.iloc[0]

            signal = row.get("signal", "Unknown")
            strength = row.get("strength", "N/A")
            ai_score = row.get("ai_score", "N/A")
            time = row.get("time", "Unknown")

            # Compute signal strength %
            score_percent = compute_signal_strength(row)

            if isinstance(time, pd.Timestamp):
                time = time.strftime("%Y-%m-%d %H:%M:%S")

            st.success(f"🟢 Signal: **{signal.upper()}**")
            st.write(f"📈 Strength: `{score_percent}`")
            st.write(f"🤖 AI Score: `{ai_score}`")
            st.write(f"🕒 Time: `{time}`")
        else:
            st.warning("⚠️ No signal yet")
            st.caption("🔄 Waiting for new analysis...")

# Display other sidebar pages (for future extension)
if page == "💬 Market Sentiment":
    st.title("📰 Market Sentiment Analysis")
    st.info("This section will analyze real-time news & sentiment using AI and NewsAPI.")
    st.caption("Coming soon...")

elif page == "📉 Technical Analysis":
    st.title("📊 Technical Indicator Analysis")
    st.info("Here you'll see detailed RSI, MACD, EMA, Fib levels, etc.")

# Usage example within your existing dashboard code:
if 'symbols' in df.columns:
    show_technical_analysis(df)
else:
    st.warning("No valid data available for technical analysis.")

if page == "🔁 Backtesting":
    st.title("🔄 Backtesting Engine")
    st.info("Compare historical signal results and strategy performance here.")
    st.caption("Coming soon...")

if page == "📈 Performance Overview":
    st.title("📌 Performance Dashboard")
    st.info("Track wins/losses, hit ratio, SL/TP outcomes, and PnL tracking.")
    st.caption("Coming soon...")

# === ENHANCEMENT END ===

# ===== Scoring logic for signal strength =====
def calculate_signal_strength(row):
    score = 0
    max_score = 100

    indicators_used = {
        "RSI": 15,
        "MACD": 15,
        "EMA": 10,
        "SMC": 20,
        "Fibonacci": 20,
        "SupportResistance": 20,
    }

    if row.get("RSI_signal") in ["buy", "sell"]:
        score += indicators_used["RSI"]
    if row.get("MACD_signal") in ["buy", "sell"]:
        score += indicators_used["MACD"]
    if row.get("EMA_signal") in ["buy", "sell"]:
        score += indicators_used["EMA"]
    if row.get("SMC_signal") in ["buy", "sell"]:
        score += indicators_used["SMC"]
    if row.get("Fibonacci_signal") in ["buy", "sell"]:
        score += indicators_used["Fibonacci"]
    if row.get("SupportResistance_signal") in ["buy", "sell"]:
        score += indicators_used["SupportResistance"]

    return min(score, max_score)

csv_path = config.SIGNAL_LOG_CSV_PATH
df = pd.read_csv(csv_path)

# Calculate signal strength
df["Signal Strength"] = df.apply(calculate_signal_strength, axis=1)

# Show latest signals
st.subheader("📡 Latest Signals")
for _, row in df.tail(10).iterrows():
    with st.expander(f"🧾 {row['symbol']} - {row['signal_type']} ({row['timeframe']})"):
        st.write(f"🕒 Time: {row['time']}")
        st.write(f"📈 Signal: {row['signal_type'].capitalize()}")
        st.write(f"📊 Strength: `{row['Signal Strength']}/100`")
        st.progress(row['Signal Strength'], text=f"{row['Signal Strength']}% strength")

with st.sidebar:
    st.title("📊 DGFXBot Dashboard")
    st.markdown("### Navigation")
    st.markdown("🔍 [Market Sentiment](#)")
    st.markdown("🧠 [Technical Analysis](#)")
    st.markdown("🧪 [Backtesting](#)")
    st.markdown("📈 [Performance Tracker](#)")
    st.markdown("✅ [Signal Feed](#)")
    st.markdown("---")
    st.markdown(f"⏱️ Auto-refresh every {config.DASHBOARD_REFRESH_INTERVAL} secs")


# Assume df is your DataFrame with all the data loaded there
# And 'symbol' column exists

def show_technical_analysis(df):
    # List of pairs
    symbols = [
        "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD",
        "USD/CAD", "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY",
        "EUR/CHF", "AUD/JPY", "GBP/CHF", "CHF/JPY", "AUD/CAD",
        "EUR/AUD", "EUR/CAD", "USD/MXN", "USD/BRL", "USD/SGD", “BTC/USD”
    ]
    
    # Select symbol
    selected_symbol = st.selectbox("Select a Symbol for Detailed Analysis", options=symbols)
    
    # Filter data for selected symbol
    symbol_data = df[df['symbol'] == selected_symbol]
    if symbol_data.empty:
        st.warning("No data available for this symbol.")
        return
    
    # Sort by time
    symbol_data = symbol_data.sort_values('time')
    
    # Latest data point
    latest = symbol_data.iloc[-1]
    
    # Show key indicators
    col1, col2, col3 = st.columns(3)
    
    # Helper function for trend
    def determine_trend(value):
        try:
            val = float(value)
            if val > 70:
                return "Overbought"
            elif val < 30:
                return "Oversold"
            else:
                return "Neutral"
        except:
            return "N/A"
    
    with col1:
        rsi = latest.get('RSI', 'N/A')
        rsi_trend = determine_trend(rsi)
        st.metric("RSI", rsi, delta=rsi_trend, delta_color='inverse')
        
    with col2:
        macd = latest.get('MACD', 'N/A')
        macd_trend = determine_trend(macd)
        st.metric("MACD", macd, delta=macd_trend, delta_color='inverse')
        
    with col3:
        ema = latest.get('EMA', 'N/A')
        ema_trend = determine_trend(ema)
        st.metric("EMA", ema, delta=ema_trend, delta_color='inverse')
    
    # Support, Resistance, Fibonacci, SMC
    if 'support_resistance' in df.columns:
        support_resistance = latest.get('support_resistance', 'N/A')
        st.markdown(f"### Support & Resistance: {support_resistance}")
        
    if 'Fibonacci' in df.columns:
        fibonacci_level = latest.get('Fibonacci', 'N/A')
        st.markdown(f"### Fibonacci Retracement Level: {fibonacci_level}")
    
    if 'SMC' in df.columns:
        smc = latest.get('SMC', 'N/A')
        st.markdown(f"### SMC Signal: {smc}")
    
    # Plot indicators over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=symbol_data['time'], y=symbol_data['RSI'], name='RSI'))
    fig.add_trace(go.Scatter(x=symbol_data['time'], y=symbol_data['MACD'], name='MACD'))
    fig.add_trace(go.Scatter(x=symbol_data['time'], y=symbol_data['EMA'], name='EMA'))
    st.plotly_chart(fig, use_container_width=True)
    
    # Plot price with overlays (assuming price data is available)
    if 'close' in symbol_data.columns:
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=symbol_data['time'], y=symbol_data['close'], name='Close Price'))
        # Optional: Add support/resistance levels
        if 'support_resistance' in symbol_data.columns:
            support = support_resistance
            # For example, if support/resistance are numeric levels
            try:
                support_level = float(support)
                fig_price.add_hline(y=support_level, line=dict(color='green', dash='dash'), annotation_text='Support')
            except:
                pass
        st.plotly_chart(fig_price, use_container_width=True)
    
    # Generate simple buy/sell signals based on indicator thresholds
    st.subheader("Trading Signals")
    signals = []
    # Example logic: RSI <30 -> Buy, RSI >70 -> Sell
    last_rsi = rsi
    if last_rsi != 'N/A':
        try:
            last_rsi_value = float(last_rsi)
            if last_rsi_value < 30:
                signals.append("Potential Buy Signal (RSI Oversold)")
            elif last_rsi_value > 70:
                signals.append("Potential Sell Signal (RSI Overbought)")
        except:
            pass
    # Similar logic can be added for MACD, EMA crossovers, etc.
    
    for s in signals:
        st.success(s)
    
    # Add your own advanced signal logic as needed

# Usage in your main app
if page == "📉 Technical Analysis":
    st.title("📊 Technical Indicator Detailed Analysis")
    show_technical_analysis(df)

# Initialize NewsAPI client (replace 'YOUR_NEWSAPI_KEY' with your real API key)
newsapi = NewsApiClient(api_key='1e7d1c0997e0421dbd4ce2049b982888')

# Load sentiment analysis pipeline
# Using a pre-trained sentiment model
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def fetch_news(query, from_date, to_date, max_articles=20):
    """Fetch latest news articles related to the query."""
    all_articles = newsapi.get_everything(q=query,
                                          from_param=from_date,
                                          to=to_date,
                                          language='en',
                                          sort_by='relevancy',
                                          page_size=max_articles)
    articles = all_articles['articles']
    # Extract relevant data
    data = []
    for article in articles:
        data.append({
            'title': article['title'],
            'description': article['description'],
            'publishedAt': article['publishedAt'],
            'content': article['content'],
            'source': article['source']['name']
        })
    return pd.DataFrame(data)


def analyze_sentiment(texts):
    """Analyze sentiment for a list of texts."""
    sentiments = sentiment_model(texts)
    return sentiments


def get_news_and_sentiment(query, days=1):
    """Fetch news from last 'days' and analyze sentiment."""
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(days=days)
    df_news = fetch_news(query, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
    if df_news.empty:
        return df_news, pd.DataFrame()

    # Combine title and description for sentiment analysis
    df_news['combined_text'] = (df_news['title'].fillna('') + ' ' + df_news['description'].fillna(''))

    # Run sentiment analysis
    sentiments = analyze_sentiment(df_news['combined_text'].tolist())

    # Add sentiment labels and scores
    df_news['sentiment_label'] = [s['label'] for s in sentiments]
    df_news['sentiment_score'] = [s['score'] for s in sentiments]
    return df_news

def plot_sentiment_over_time(df_news):
    """Plot sentiment scores over time."""
    if df_news.empty:
        st.write("No news data to plot.")
        return
    df_news['publishedAt'] = pd.to_datetime(df_news['publishedAt'])
    df_news = df_news.sort_values('publishedAt')

    # Aggregate by day
    df_daily = df_news.resample('D', on='publishedAt').mean()

    plt.figure(figsize=(10, 4))
    plt.plot(df_daily.index, df_daily['sentiment_score'], marker='o')
    plt.title("Average Sentiment Score Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.ylim(0, 1)
    plt.grid(True)
    st.pyplot(plt)

def display_top_news(df_news, top_n=5):
    """Display top positive and negative news."""
    if df_news.empty:
        st.write("No news articles for display.")
        return
    # Top positive news
    top_positive = df_news[df_news['sentiment_label'] == 'POSITIVE'].nlargest(top_n, 'sentiment_score')
    # Top negative news
    top_negative = df_news[df_news['sentiment_label'] == 'NEGATIVE'].nsmallest(top_n, 'sentiment_score')

    st.subheader("Top Positive News")
    for idx, row in top_positive.iterrows():
        st.markdown(f"**{row['title']}**\n*Source:* {row['source']}\n*Published:* {row['publishedAt']}\n\n")

    st.subheader("Top Negative News")
    for idx, row in top_negative.iterrows():
        st.markdown(f"**{row['title']}**\n*Source:* {row['source']}\n*Published:* {row['publishedAt']}\n\n")

# --- Streamlit App ---
st.title("Market Sentiment Analysis Dashboard")

# User input for symbol or market
market_query = st.text_input("Enter Market/Asset for Sentiment Analysis (e.g., 'Stock Market', 'Bitcoin')", "Stock Market")
days = st.slider("Days of news to analyze", 1, 7, 1)

# Fetch and analyze news
if st.button("Fetch & Analyze News"):
    with st.spinner("Fetching news articles..."):
        news_df = get_news_and_sentiment(market_query, days=days)

    if news_df.empty:
        st.warning("No news articles found for this query and date range.")
    else:
        st.success(f"Found {len(news_df)} news articles. Analyzing sentiment...")

        # Show sentiment summary
        sentiment_counts = news_df['sentiment_label'].value_counts()
        st.write("Sentiment Distribution:")
        st.bar_chart(sentiment_counts)

        # Show sentiment score trend over time
        plot_sentiment_over_time(news_df)

        # Show top positive and negative news
        display_top_news(news_df)

# Optional: add auto-refresh, more filters, or detailed text analysis
