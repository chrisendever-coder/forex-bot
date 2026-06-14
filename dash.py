import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Premium Signal Panel", layout="wide")

# --- MASTER PASSWORDS ---
VALID_PASSWORDS = ["GOLD2026", "VIPTRADE", "BTCPRO"]

# --- LOGIN SCREEN INTERFACE (USES FULL SCREEN WIDTH) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Premium Trading Signals Portal")
    st.write("Welcome! Enter your premium member password below to unlock the terminal.")
    
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

# --- ULTRA COMPACT SPLIT SCREEN (ONLY SPLITS AFTER UNLOCK) ---
st.title("📊 Institutional Signal Terminal")

left_side, right_side = st.columns([1, 2]) # 1 part controls, 2 parts data display

with left_side:
    st.subheader("⚙️ Settings")
    asset = st.selectbox("Asset", ["BTC-USD", "ETH-USD", "XAUUSD=X", "EURUSD=X"])
    tf = st.selectbox("Time Frame", ["1m", "5m", "15m", "1h", "1d"])
    tp_percent = st.slider("TP %", min_value=0.5, max_value=5.0, value=2.0, step=0.1) / 100
    sl_percent = st.slider("SL %", min_value=0.5, max_value=5.0, value=1.0, step=0.1) / 100
    if st.button("🔒 Lock Screen"):
        st.session_state["authenticated"] = False
        st.rerun()

with right_side:
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
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Price", f"${current_price:.2f}")
            m2.metric("MA(14)", f"${current_sma:.2f}")
            m3.metric("TP", f"${tp_level:.2f}")
            m4.metric("SL", f"${sl_level:.2f}")
            
            if current_price > current_sma:
                st.success(f"🟩 BUY TREND ({tf})")
            elif current_price < current_sma:
                st.error(f"🟥 SELL TREND ({tf})")
            else:
                st.warning("⬜ NO SIGNAL")
                
            st.line_chart(df[['Close', 'SMA']].tail(35), height=250)
        else:
            st.error("Market closed. Try 'BTC-USD'.")
    except Exception as e:
        st.error(f"Error: {e}")