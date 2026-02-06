import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Styling
st.markdown("<style>.crude-box { background-color: #1a1a1a; padding: 20px; border-radius: 10px; border: 2px solid #ffca28; }</style>", unsafe_allow_html=True)

st.title("📟 MCX & Nifty Live Scanner")

# --- CRUDE OIL SECTION ---
def get_crude_signal():
    try:
        # CL=F is International Crude, MCX ke liye hum ise base maante hain
        crude = yf.Ticker("CL=F") 
        df = crude.history(period="1d", interval="5m")
        if not df.empty:
            cmp = round(df['Close'].iloc[-1], 2)
            high = df['High'].max()
            low = df['Low'].min()
            
            # Tradex Style Logic
            if cmp < low * 1.005:
                signal = "BEARISH"
                level = f"BELOW {round(low, 2)}"
                color = "#e74c3c"
            elif cmp > high * 0.995:
                signal = "BULLISH"
                level = f"ABOVE {round(high, 2)}"
                color = "#2ecc71"
            else:
                signal = "NEUTRAL"
                level = "WAIT FOR BREAKOUT"
                color = "#ffca28"
            
            return cmp, signal, level, color
    except:
        return None, "DATA ERROR", "-", "#fff"

cmp, signal, level, color = get_crude_signal()

if cmp:
    st.markdown(f"""
        <div class='crude-box'>
            <h2 style='margin:0;'>CRUDE OIL FUT</h2>
            <h1 style='color:{color}; margin:10px 0;'>{signal} {level}</h1>
            <p style='font-size:20px;'>Current Market Price: <b>{cmp}</b></p>
        </div>
    """, unsafe_allow_html=True)

# ... (Baaki Nifty 50 wala table niche chalta rahega)
