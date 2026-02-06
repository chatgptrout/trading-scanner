import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH COMMANDER", layout="wide")

# CSS for all features
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; border-radius: 12px; padding: 15px; border-left: 8px solid #00f2ff; margin-bottom: 10px; }</style>""", unsafe_allow_html=True)

# --- SECTION 1: NIFTY & BANK NIFTY TREND (From image_1feeca.png) ---
st.markdown("<h2 style='color:#00f2ff;'>📊 INDEX TREND & PCR</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: st.markdown('<div class="card"><b>NIFTY PCR</b><br><h2 style="color:#00ff88">1.15 (Bullish)</h2></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="card"><b>BANK NIFTY</b><br><h2 style="color:#ff4b2b">Bearish 🔴</h2></div>', unsafe_allow_html=True)

# --- SECTION 2: TRADEX STYLE REVERSAL (From image_1000104527.jpg) ---
st.markdown("<h2 style='color:#00f2ff;'>🎯 TRADEX REVERSAL LEVELS</h2>", unsafe_allow_html=True)
def get_reversal(sym):
    df = yf.download(sym, period='2d', interval='15m', progress=False)
    pivot = (df['High'].iloc[-2] + df['Low'].iloc[-2] + df['Close'].iloc[-2]) / 3
    s1 = (2 * pivot) - df['High'].iloc[-2]
    return pivot, s1

try:
    p_nifty, s1_nifty = get_reversal("^NSEI")
    st.success(f"NIFTY Reversal Possible From: ₹{s1_nifty:.2f}")
except: st.write("Calculating levels...")

# --- SECTION 3: STOCK SCANNER (From image_1000104522.jpg) ---
st.markdown("<h2 style='color:#00f2ff;'>🦅 LIVE STOCK SIGNALS</h2>", unsafe_allow_html=True)
tickers = ["RELIANCE.NS", "SBIN.NS", "ZOMATO.NS", "TATAMOTORS.NS"]
for sym in tickers:
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        change = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        color = "#00ff88" if change > 0 else "#ff4b2b"
        st.markdown(f'<div class="card" style="border-left-color:{color}"><h3>{sym}: ₹{p:.2f} ({change:.2f}%)</h3></div>', unsafe_allow_html=True)
    except: continue

time.sleep(20)
st.rerun()
