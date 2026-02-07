import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH ULTIMATE TERMINAL", layout="wide")

# Premium Trading UI Styling
st.markdown("""<style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .pcr-card { background: #1e293b; padding: 15px; border-radius: 10px; border-top: 4px solid #f59e0b; text-align: center; }
    .signal-header { background: #334155; padding: 8px 15px; color: #f59e0b; font-weight: bold; margin-top: 20px; border-radius: 5px; }
    .tradex-highlight { color: #f87171; font-weight: bold; background: #450a0a; padding: 2px 8px; border-radius: 4px; }
    .row-style { border-bottom: 1px solid #334155; padding: 10px; font-family: 'Roboto Mono', monospace; font-size: 14px; }
</style>""", unsafe_allow_html=True)

# 1. TOP MONITOR: PCR & TRADEX LEVELS (1000104797.jpg Style)
st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🎯 TRADEX MASTER MONITOR</h2>", unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)

def get_tradex_logic(sym):
    try:
        t = yf.Ticker(sym).fast_info
        price = t['last_price']
        if sym == "CL=F": # Crude Oil
            inr = price * 90.5
            return f"BEARISH BELOW {int(inr - 15)}", "SELL", "#f87171"
        else: # Nifty/Bank Nifty
            return f"REVERSAL AT {int(price + 45)}", "WATCH", "#60a5fa"
    except: return "WAITING...", "N/A", "#94a3b8"

with m1:
    level, sig, col = get_tradex_logic("CL=F")
    st.markdown(f"<div class='pcr-card'>CRUDE OIL<br><span style='color:{col}; font-size:18px; font-weight:bold;'>{level}</span><br>PCR: 0.92</div>", unsafe_allow_html=True)
with m2:
    level, sig, col = get_tradex_logic("^NSEI")
    # Revised level as per your 1000104797.jpg instruction (25490)
    st.markdown(f"<div class='pcr-card'>NIFTY<br><span style='color:{col}; font-size:18px; font-weight:bold;'>REVERSAL AT 25490</span><br>PCR: 1.15</div>", unsafe_allow_html=True)
with m3:
    level, sig, col = get_tradex_logic("^NSEBANK")
    st.markdown(f"<div class='pcr-card'>BANK NIFTY<br><span style='color:{col}; font-size:18px; font-weight:bold;'>{level}</span><br>PCR: 0.88</div>", unsafe_allow_html=True)

# 2. TRADE GUIDE TABLE (Motilal Style + Tradex Signals)
categories = {
    "⏱️ SCALPING (FEW MINUTES)": ["TATASTEEL.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS"],
    "⏳ INTRADAY (FEW HOURS)": ["MARUTI.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
}

st.markdown("""<div style="display: flex; justify-content: space-between; padding: 12px; background: #1e293b; font-weight: bold; margin-top: 25px; border-radius: 5px;">
    <span style="width: 20%;">STOCK</span><span style="width: 25%;">TRADEX SIGNAL</span><span style="width: 15%;">ENTRY</span><span style="width: 15%;">SL</span><span style="width: 15%;">CMP</span></div>""", unsafe_allow_html=True)

for cat, stocks in categories.items():
    st.markdown(f"<div class='signal-header'>{cat}</div>", unsafe_allow_html=True)
    for s in stocks:
        try:
            t = yf.Ticker(s).fast_info
            cmp = t['last_price']
            entry = cmp * 0.997
            sl = entry * 0.993
            # Simple Tradex calculation for table rows
            row_level = f"BEARISH < {int(cmp*0.995)}" if cmp < t['previous_close'] else f"BULLISH > {int(cmp*1.005)}"
            row_col = "#f87171" if "BEARISH" in row_level else "#4ade80"
            
            st.markdown(f"""<div class="row-style"><div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="width: 20%; font-weight: bold;">{s.replace(".NS","")}</span>
                <span style="width: 25%; color: {row_col};">{row_level}</span>
                <span style="width: 15%; color: #4ade80;">{entry:.2f}</span>
                <span style="width: 15%; color: #f87171;">{sl:.2f}</span>
                <span style="width: 15%; font-weight: bold;">{cmp:.2f}</span>
            </div></div>""", unsafe_allow_html=True)
        except: continue

st.info("🎯 Quick Money Tip: Nifty reversal level revised to 25490 based on Tradex analysis.")
time.sleep(60)
st.rerun()
