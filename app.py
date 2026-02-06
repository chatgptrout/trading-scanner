import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(layout="wide", page_title="Santosh Pro Terminal")

# Professional Dark Style
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .crude-card { background-color: #111; padding: 20px; border: 2px solid #ffca28; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border: 0.5px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. CRUDE OIL SIGNAL LOGIC
def get_crude_data():
    try:
        crude = yf.Ticker("CL=F")
        df = crude.history(period="1d", interval="5m")
        if not df.empty:
            cmp = round(df['Close'].iloc[-1], 2)
            low = round(df['Low'].min(), 2)
            high = round(df['High'].max(), 2)
            if cmp < low * 1.005: return cmp, "BEARISH", f"BELOW {low}", "#e74c3c"
            if cmp > high * 0.995: return cmp, "BULLISH", f"ABOVE {high}", "#2ecc71"
            return cmp, "NEUTRAL", "WAIT", "#ffca28"
    except: return None, "OFFLINE", "-", "#555"
    return None, None, None, None

# 2. NIFTY 50 DATA LOGIC
nifty50_list = ["RELIANCE", "TCS", "HDFCBANK", "SBIN", "ICICIBANK", "TATAMOTORS", "INFY", "AXISBANK", "DLF", "GNFC"] # Add more as needed

def get_table_data():
    rows = []
    data = yf.download([t + ".NS" for t in nifty50_list], period="2d", group_by='ticker', progress=False)
    for t in nifty50_list:
        try:
            df = data[t + ".NS"]
            cmp = round(df['Close'].iloc[-1], 2)
            open_p = df['Open'].iloc[-1]
            action = "BUY EXIT" if cmp > open_p else "SELL EXIT"
            trend = "Positive" if cmp > df['Close'].iloc[-2] else "Negative"
            rows.append({
                "Action": action, "Symbol": t, "Entry": round(open_p, 2), "CMP": cmp,
                "Target": round(cmp * 1.015, 2) if action == "BUY EXIT" else round(cmp * 0.985, 2),
                "Trend": trend, "Valuation": "Attractive" if trend == "Positive" else "Fair"
            })
        except: continue
    return pd.DataFrame(rows)

# --- DISPLAY ---
st.title("📟 Santosh Multi-Scanner Terminal")

# A. Crude Section (Upar)
c_cmp, c_sig, c_lvl, c_col = get_crude_data()
if c_cmp:
    st.markdown(f"<div class='crude-card'><h2 style='margin:0;'>CRUDE OIL FUT</h2><h1 style='color:{c_col};'>{c_sig} {c_lvl}</h1><p>Price: {c_cmp}</p></div>", unsafe_allow_html=True)

# B. Market Breadth & Table (Niche)
df_final = get_table_data()
if not df_final.empty:
    col_chart, col_extra = st.columns([1, 2])
    with col_chart:
        pos = len(df_final[df_final['Trend'] == 'Positive'])
        neg = len(df_final[df_final['Trend'] == 'Negative'])
        fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[pos, neg], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
        fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📊 Trade Guide (Motilal Style)")
    def style_table(val):
        if val == 'BUY EXIT': return 'background-color: #1b5e20; color: white;'
        if val == 'SELL EXIT': return 'background-color: #b71c1c; color: white;'
        return ''
    
    st.table(df_final.style.map(style_table, subset=['Action']))

# AUTO REFRESH
time.sleep(60)
st.rerun()
