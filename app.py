import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH AI TRADEX", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .reversal-card { 
        background: linear-gradient(145deg, #0d1b2a, #16213e); 
        padding: 20px; border-radius: 15px; 
        border: 2px solid #00f2ff; margin-bottom: 15px;
        box-shadow: 0px 0px 15px #00f2ff;
    }
    .level-text { font-size: 24px; font-weight: bold; color: #00ff88; }
    </style>
    """, unsafe_allow_html=True)

# Nifty aur Bank Nifty ke liye special tracking
indices = ["^NSEI", "^NSEBANK"]

st.markdown("<h1 style='text-align:center;'>🎯 AI REVERSAL TRACKER (TRADEX STYLE)</h1>", unsafe_allow_html=True)

for sym in indices:
    try:
        # Reversal nikalne ke liye pichle din ka data zaroori hai
        df = yf.download(sym, period='2d', interval='15m', progress=False)
        if not df.empty:
            # Pivot Point Calculation (Traditional)
            high = df['High'].iloc[-2]
            low = df['Low'].iloc[-2]
            close = df['Close'].iloc[-2]
            pivot = (high + low + close) / 3
            s1 = (2 * pivot) - high  # Support 1 (Yahan se reversal possible hai)
            
            curr_price = df['Close'].iloc[-1]
            name = "NIFTY" if sym == "^NSEI" else "BANK NIFTY"
            
            st.markdown(f"""
                <div class="reversal-card">
                    <h2 style="margin:0;">{name} LIVE: ₹{curr_price:.2f}</h2>
                    <p style="font-size:18px; color:#a0a0a0;">Current Sentiment: {"BULLISH 🐂" if curr_price > pivot else "BEARISH 🐻"}</p>
                    <hr style="border:0.5px solid #1e3a5f">
                    <div style="display:flex; justify-content:space-between">
                        <div>
                            <span style="color:#ff4b2b">REVERSAL POSSIBLE FROM:</span><br>
                            <span class="level-text">₹{s1:.2f}</span>
                        </div>
                        <div style="text-align:right">
                            <span style="color:#00ff88">PIVOT LEVEL:</span><br>
                            <span style="font-size:20px; font-weight:bold">₹{pivot:.2f}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    except:
        continue

time.sleep(15)
st.rerun()
