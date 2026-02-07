import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH TRADE GUIDE PRO", layout="wide")

# Motilal Oswal Premium Dark Style
st.markdown("""<style>
    .stApp { background-color: #121212; color: #ffffff; }
    .pcr-box { background: #262626; padding: 15px; border-radius: 8px; border-top: 4px solid #ffcc00; text-align: center; }
    .pcr-val { font-size: 22px; font-weight: bold; color: #ffcc00; }
    .cat-header { background: #333333; padding: 8px 15px; color: #ffcc00; font-weight: bold; margin-top: 20px; border-radius: 5px; }
    .data-row { border-bottom: 1px solid #444; padding: 10px; font-family: monospace; }
</style>""", unsafe_allow_html=True)

# 1. PCR & MARKET STRIP (Top Section)
st.markdown("<h2 style='text-align:center; color:#ffcc00;'>📊 MARKET MONITOR + PCR</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

def get_pcr(sym):
    # Simulating PCR logic for display (Actual PCR requires Option Chain API)
    # In live market, this would fetch Put OI / Call OI
    return 1.25 if sym == "^NSEI" else 0.85

with c1:
    pcr_nifty = get_pcr("^NSEI")
    st.markdown(f"<div class='pcr-box'>NIFTY PCR<br><span class='pcr-val'>{pcr_nifty}</span><br><small>BULLISH</small></div>", unsafe_allow_html=True)
with c2:
    pcr_bn = get_pcr("^NSEBANK")
    st.markdown(f"<div class='pcr-box'>BANK NIFTY PCR<br><span class='pcr-val'>{pcr_bn}</span><br><small>BEARISH</small></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pcr-box'>MARKET SENTIMENT<br><span class='pcr-val' style='color:#00ff88;'>BUY ON DIPS</span></div>", unsafe_allow_html=True)

# 2. TRADE GUIDE TABLE (Motilal Style)
categories = {
    "🔥 SCALPING (FEW MINUTES)": ["TATASTEEL.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS"],
    "⏳ INTRADAY (FEW HOURS)": ["MARUTI.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
}

def fetch_data(symbol):
    try:
        t = yf.Ticker(symbol).fast_info
        cmp = t['last_price']
        entry = cmp * 0.996
        sl = entry * 0.992
        return {"name": symbol.replace(".NS",""), "entry": entry, "sl": sl, "cmp": cmp}
    except: return None

st.markdown("""<div style="display: flex; justify-content: space-between; padding: 10px; background: #262626; font-weight: bold; margin-top: 20px;">
    <span style="width: 25%;">STOCK</span><span style="width: 20%;">ENTRY</span><span style="width: 20%;">STOP LOSS</span><span style="width: 20%;">CMP</span></div>""", unsafe_allow_html=True)

for cat, stocks in categories.items():
    st.markdown(f"<div class='cat-header'>{cat}</div>", unsafe_allow_html=True)
    for s in stocks:
        d = fetch_data(s)
        if d:
            color = "#00ff88" if d['cmp'] > d['entry'] else "#ff4b2b"
            st.markdown(f"""<div class="data-row"><div style="display: flex; justify-content: space-between;">
                <span style="width: 25%; font-weight: bold;">{d['name']}</span>
                <span style="width: 20%; color: #00ff88;">{d['entry']:.2f}</span>
                <span style="width: 20%; color: #ff4b2b;">{d['sl']:.2f}</span>
                <span style="width: 20%; color: {color};">{d['cmp']:.2f}</span>
            </div></div>""", unsafe_allow_html=True)

time.sleep(60)
st.rerun()
