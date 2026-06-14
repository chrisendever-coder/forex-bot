import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Premium Signal Panel", layout="wide")

# --- MASTER PASSWORDS ---
VALID_PASSWORDS = ["GOLD2026", "VIPTRADE", "BTCPRO"]

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- LOGIN SCREEN INTERFACE ---
if not st.session_state["authenticated"]:
    st.title("🔒 Premium Trading Signals Portal")
    st.write("Enter your premium member password below to unlock the terminal.")
    
    if st.button("🚀 Fast Admin Bypass Login"):
        st.session_state["authenticated"] = True
        st.rerun()
        
    user_input = st.text_input("Enter Premium Password", type="password")
    if st.button("Unlock Dashboard"):
        if user_input in VALID_PASSWORDS:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Invalid Password.")
    st.stop()

# --- MAIN DASHBOARD INTERFACE (UNLOCKED) ---
st.title("📊 Institutional Signal Software Dashboard")

if st.button("🔒 Log Out / Lock Screen"):
    st.session_state["authenticated"] = False
    st.rerun()

st.write("---")

# ⚙️ Configuration Pickers
asset = st.selectbox("Select Asset Class", ["BTC-USD", "ETH-USD", "XAUUSD=X", "EURUSD=X", "GBPUSD=X", "USDJPY=X"])
tf = st.selectbox("Select Time Frame", ["1m", "5m", "15m", "1h", "1d"])

# 🛡️ Risk Management Parameters
tp_percent = st.slider("Take Profit Target (TP %)", min_value=0.5, max_value=5.0, value=2.0, step=0.1) / 100
sl_percent = st.slider("Stop Loss Risk (SL %)", min_value=0.5, max_value=5.0, value=1.0, step=0.1) / 100

st.write("---")
st.subheader(f"📈 Analytics Market Feed: {asset} ({tf} Chart)")

history_window = "1d" if tf in ["1m", "5m", "15m"] else "1mo"

try:
    ticker = yf.Ticker(asset)
    df = ticker.history(period=history_window, interval=tf)
    
    if not df.empty:
        df['SMA'] = df['Close'].rolling(window=14).mean()
        current_price = df['Close'].iloc[-1]
        current_sma = df['SMA'].iloc[-1]
        
        # Calculate Risk Management targets
        tp_level = current_price * (1 + tp_percent)
        sl_level = current_price * (1 - sl_percent)
        
        # Large Metric Counters
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Live Price", f"${current_price:.2f}")
        m2.metric("Trend line (MA)", f"${current_sma:.2f}")
        m3.metric("🟢 Take Profit (TP)", f"${tp_level:.2f}")
        m4.metric("🔴 Stop Loss (SL)", f"${sl_level:.2f}")
        
        # Strategy Signal Banner
        if current_price > current_sma:
            st.success(f"🟩 SIGNAL: BUY TREND — Market is holding above the {tf} Moving Average line.")
        elif current_price < current_sma:
            st.error(f"🟥 SIGNAL: SELL TREND — Market is breaking below the {tf} Moving Average line.")
        else:
            st.warning("⬜ SIGNAL: NO TREND")
            
        # Financial Trend Graph Chart
        chart_data = df[['Close', 'SMA']].tail(60)
        st.line_chart(chart_data)
        
    else:
        st.error(f"⚠️ {asset} market data feed is temporarily empty due to weekend market closure.")
except Exception as e:
    st.error(f"Dashboard system link error: {e}")