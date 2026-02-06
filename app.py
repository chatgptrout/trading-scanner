import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH PRO COMMANDER", layout="wide")

# CSS
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; border-radius: 12px; padding: 15px; border-left: 8px solid #00f2ff; margin-bottom: 10px; }</style>""", unsafe_allow_html=True)

# 1. INDEX TREND (Nifty/BankNifty)
st.markdown("<h2 style='color:#00f2ff;'>📊 INDEX TREND & PCR</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: st.markdown('<div class="card"><b>NIFTY PCR</b><br><h2 style="color:#00ff88">1.15 (Bullish)</h2></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="card"><b>BANK NIFTY</b><br><h2 style="color:#ff4b2b">Bearish 🔴</h2></div>', unsafe_allow_html=True)

# 2. TRADEX REVERSAL LEVELS (image_1000104527.jpg)
st.markdown("<h2 style='color:#00f2ff;'>🎯 REVERSAL LEVELS (TRADEX STYLE)</h2>", unsafe_allow_html=True)
def get_reversal(sym):
    df = yf.download(sym, period='2d', interval='15m', progress=False)
    pivot = (df['High'].iloc[-2] + df['Low'].iloc[-2] + df['Close'].iloc[-2]) / 3
    s1 = (2 * pivot) - df['High'].iloc[-2]
    return s1

try:
    s1_nifty = get_reversal("^NSEI")
    st.info(f"NIFTY Reversal Level: ₹{s1_nifty:.2f}")
except: st.write("Loading levels...")

# 3. HIGH MOVEMENT STOCKS + TARGET/SL (image_1000104522.jpg)
st.markdown("<h2 style='color:#00f2ff;'>🦅 HIGH MOMENTUM SIGNALS (TARGET/SL)</h2>", unsafe_allow_html=True)
# List of high volatility stocks
tickers = ["RELIANCE.NS", "SBIN.NS", "ZOMATO.NS", "TATAMOTORS.NS", "HAL.NS", "DIXON.NS", "ADANIENT.NS"]

for sym in tickers:
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        change = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        # MOVEMENT FILTER: Sirf wahi dikhao jo 0.7% se zyada hile hain
        if abs(change) > 0.7:
            color = "#00ff88" if change > 0 else "#ff4b2b"
            action = "BUY" if change > 0 else "SELL"
            
            # Target (1%) and SL (0.5%)
            target = p * 1.01 if action == "BUY" else p * 0.99
            sl = p * 0.995 if action == "BUY" else p * 1.005
            
            st.markdown(f"""
                <div class="card" style="border-left-color:{color}">
                    <h3 style="margin:0;">{action}: {sym} | Price: ₹{p:.2f} ({change:.2f}%)</h3>
                    <p style="color:{color}; font-size:18px; font-weight:bold;">🎯 Target: ₹{target:.2f} | 🛑 SL: ₹{sl:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
    except: continue

time.sleep(15)
st.rerun()# --- NeoTrader Style Multi-Target Logic ---
def get_neo_signal(sym):
    t = yf.Ticker(sym)
    p = t.fast_info['last_price']
    c = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
    
    # High Movement Filter (Neo Style)
    if abs(c) > 0.8:
        color = "#00ff88" if c > 0 else "#ff4b2b"
        # 3 Targets like NeoTrader (T1=0.5%, T2=1%, T3=1.5%)
        t1 = p * 1.005 if c > 0 else p * 0.995
        t2 = p * 1.01 if c > 0 else p * 0.99
        t3 = p * 1.015 if c > 0 else p * 0.985
        sl = p * 0.994 if c > 0 else p * 1.006
        
        st.markdown(f"""
            <div class="card" style="border-left:10px solid {color}">
                <h3 style="margin:0;">🚀 {sym} @ ₹{p:.2f}</h3>
                <p style="color:{color}; font-weight:bold;">T1: ₹{t1:.2f} | T2: ₹{t2:.2f} | T3: ₹{t3:.2f}</p>
                <p style="color:white;">Stop Loss: ₹{sl:.2f}</p>
            </div>
        """, unsafe_allow_html=True)

