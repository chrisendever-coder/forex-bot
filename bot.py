cat << 'EOF' > app.py
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Forex & Gold Signal Dashboard", layout="wide")
st.title("📊 Live Trading Signal Dashboard")

# Sidebar configurations
symbol = st.sidebar.selectbox("Select Asset", ["XAUUSD=X", "EURUSD=X", "GBPUSD=X", "JPY=X"])
sma_length = st.sidebar.slider("SMA Trend Length", min_value=5, max_value=50, value=10)

st.subheader(f"Current Status for {symbol}")

try:
    # Fetch data
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="5d", interval="1m")
    
    if not df.empty:
        # Calculate Math
        df['SMA'] = df['Close'].rolling(window=sma_length).mean()
        current_price = df['Close'].iloc[-1]
        current_sma = df['SMA'].iloc[-1]
        
        # Metric Blocks
        col1, col2 = st.columns(2)
        col1.metric("Live Price", f"${current_price:.2f}")
        col2.metric(f"SMA ({sma_length})", f"${current_sma:.2f}")
        
        # Signal Box
        if current_price > current_sma:
            st.success("🟩 SIGNAL: BUY (Bullish Trend)")
        elif current_price < current_sma:
            st.error("🟥 SIGNAL: SELL (Bearish Trend)")
        else:
            st.warning("⬜ SIGNAL: NO TREND")
            
        # Interactive Chart
        st.subheader("Recent Price Action")
        chart_data = df[['Close', 'SMA']].tail(60)
        st.line_chart(chart_data)
        
    else:
        st.info("Market is closed over the weekend. No live data stream available.")
except Exception as e:
    st.error(f"Error loading dashboard: {e}")
EOF