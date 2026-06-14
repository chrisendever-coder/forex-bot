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

# --- MAIN DASHBOARD INTERFACE (STABLE LAYOUT FOR CHROMECKEEPS) ---
st.title("📊 Institutional Signal Software Dashboard")

if st.button("🔒 Log Out / Lock Screen"):
    st.session_state["authenticated"] = False
    st.rerun()

st.write("---")

# Compact controls stacked normally to avoid screen-resize crashes
asset = st.selectbox("Select Asset Class", ["BTC-USD", "ETH-USD", "XAUUSD=X", "EURUSD=X"])
tf = st.selectbox("Select Time Frame", ["1m", "5m", "15m", "1h", "1d"])

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
        
        tp_level = current_price * (1 + tp_percent)
        sl_level = current_price * (1 - sl_percent)
        
        # Displaying metrics vertically to fit smaller screens perfectly
        st.metric("Live Price", f"${current_price:.2f}")
        st.metric("Trend line (MA)", f"${current_sma:.2f}")
        st.metric("🟢 Take Profit (TP)", f"${tp_level:.2f}")
        st.metric("🔴 Stop Loss (SL)", f"${sl_level:.2f}")
        
        if current_price > current_sma:
            st.success(f"🟩 SIGNAL: BUY TREND")
        elif current_price < current_sma:
            st.error(f"🟥 SIGNAL: SELL TREND")
        else:
            st.warning("⬜ SIGNAL: NO TREND")
            
        # Draw line chart with fixed container width turned on
        st.line_chart(df[['Close', 'SMA']].tail(40), use_container_width=True)
        
    else:
        st.error(f"⚠️ {asset} market data feed is temporarily empty due to weekend market closure.")
except Exception as e:
    st.error(f"Dashboard system link error: {e}")