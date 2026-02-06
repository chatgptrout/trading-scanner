import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Pro Master Terminal")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { 
        padding: 15px; border-radius: 8px; border: 1px solid #333; 
        text-align: center; margin-bottom: 10px; background-color: #111;
    }
    .ng-special { border: 2px solid #ffca28 !important; }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border: 0.1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic for Top Bar (Indices & Commodities)
def get_master_signals():
    tickers = {
        "NIFTY 50": "^NSEI", "SENSEX": "^BSESN", 
        "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", 
        "GOLD": "GC=F", "SILVER": "SI=F"
    }
    results = []
    for name, sym in tickers.items():
        try:
            data = yf.Ticker(sym).history(period="2d", interval="5m")
            if not data.empty:
                cmp = round(data['Close'].iloc[-1], 2)
                high, low = data['High'].max(), data['Low'].min()
                prev_close = data['Close'].iloc[-2]

                if name == "NAT GAS":
                    if cmp > (high * 0.995): status, color = "🚀 BREAKOUT", "#00ff00"
                    elif cmp < (low * 1.005): status, color = "⚠️ CRASHING", "#ff0000"
                    else: status, color = "SIDEWAYS", "#ffca28"
                else:
                    status, color = ("BULLISH", "#2ecc71") if cmp > prev_close else ("BEARISH", "#e74c3c")
                
                results.append({"name": name, "cmp": cmp, "status": status, "color": color})
        except: continue
    return results

# 3. Logic for Trade Table
nifty_list = ["RELIANCE", "TCS", "HDFCBANK", "SBIN", "ICICIBANK", "TATAMOTORS", "INFY", "DLF", "GNFC"]

def get_table_data():
    rows = []
    data = yf.download([t + ".NS" for t in nifty_list], period="2d", group_by='ticker', progress=False)
    for t in nifty_list:
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

# --- DISPLAY SECTION ---
st.title("📟 Santosh Master Dashboard")
st.write(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")

# A. TOP SIGNALS
signals = get_master_signals()
if signals:
    cols = st.columns(6)
    for i, sig in enumerate(signals):
        with cols[i]:
            card_class = "signal-card ng-special" if sig['name'] == "NAT GAS" else "signal-card"
            st.markdown(f"<div class='{card_class}'><small>{sig['name']}</small><h3 style='color:{sig['color']}; margin:5px 0;'>{sig['status']}</h3><b>{sig['cmp']}</b></div>", unsafe_allow_html=True)

st.markdown("---")

# B. BREADTH CHART & TABLE (Dono ek hi row mein)
df_final = get_table_data()
if not df_final.empty:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Nifty 50 Breadth")
        pos, neg = len(df_final[df_final['Trend'] == 'Positive']), len(df_final[df_final['Trend'] == 'Negative'])
        fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[pos, neg], hole=.7, marker_colors=['#2ecc71', '#e74c3c'])])
        fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("📊 Motilal Trade Guide")
        def style_rows(val):
            if val == 'BUY EXIT': return 'background-color: #1b5e20; color: white;'
            if val == 'SELL EXIT': return 'background-color: #b71c1c; color: white;'
            return ''
        # FIXED: Sirf ek table yahan aayega
        st.table(df_final.style.map(style_rows, subset=['Action']))

# 4. AUTO REFRESH
time.sleep(60)
st.rerun()
