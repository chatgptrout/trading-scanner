import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Volume Master", initial_sidebar_state="collapsed")

# Professional UI
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    .signal-card { 
        background-color: #fdfdfd; border-radius: 8px; padding: 15px; 
        border-left: 6px solid #2ecc71; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .vol-confirm { color: #157347; font-weight: bold; font-size: 11px; background: #d1e7dd; padding: 2px 5px; border-radius: 3px; }
    .signal-sell { border-left-color: #e74c3c; }
    </style>
    """, unsafe_allow_html=True)

# 2. Advanced Data Engine with Volume
@st.cache_data(ttl=60)
def get_volume_signals():
    watch_list = ["RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS", "POWERGRID", "LT", "SBIN", "TATAMOTORS", "ADANIENT"]
    tickers = [t + ".NS" for t in watch_list]
    raw = yf.download(tickers, period="5d", interval="15m", group_by='ticker', progress=False)
    
    signals = []
    for t in watch_list:
        try:
            df = raw[t + ".NS"].dropna()
            if df.empty: continue
            
            # Volume Check
            avg_vol = df['Volume'].tail(20).mean()
            curr_vol = df['Volume'].iloc[-1]
            vol_boost = True if curr_vol > (avg_vol * 1.5) else False
            
            cmp = round(df['Close'].iloc[-1], 2)
            chg = round(((cmp - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100, 2)
            
            if abs(chg) > 0.05:
                side = "BUY" if chg > 0 else "SELL"
                sl = round(cmp * 0.992, 2) if side == "BUY" else round(cmp * 1.008, 2)
                tgt = round(cmp * 1.02, 2) if side == "BUY" else round(cmp * 0.98, 2)
                signals.append({"name": t, "side": side, "cmp": cmp, "sl": sl, "tgt": tgt, "vol": vol_boost})
        except: continue
    return signals

# --- DISPLAY ---
st.subheader("🚀 Live Volume Breakout Signals")
active_signals = get_volume_signals()

if active_signals:
    cols = st.columns(2) # Two columns for more signals
    for i, s in enumerate(active_signals[:6]):
        with cols[i % 2]:
            border = "signal-sell" if s['side'] == "SELL" else ""
            vol_tag = "<span class='vol-confirm'>🔥 VOL CONFIRMED</span>" if s['vol'] else ""
            st.markdown(f"""
                <div class='signal-card {border}'>
                    <div style='display:flex; justify-content:space-between;'>
                        <b>{s['side']} {s['name']}</b>
                        {vol_tag}
                    </div>
                    <div style='margin-top:8px;'>
                        <b>CMP: {s['cmp']}</b> | <span style='color:#e74c3c;'>SL: {s['sl']}</span> | <span style='color:#2ecc71;'>TGT: {s['tgt']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("Scanning for Volume Breakouts...")

time.sleep(60)
st.rerun()
