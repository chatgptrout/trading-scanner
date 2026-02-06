import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(layout="wide", page_title="Santosh Pro Hybrid")

# Custom CSS for Dark UI
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    th { background-color: #222 !important; color: #ffca28 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. Top Section: IntradayPulse Style Chart ---
def draw_circular_chart(data):
    # Mapping colors for the donut chart
    colors = ['#2ecc71' if x == 'Positive' else '#e74c3c' for x in data['Financial Trend']]
    
    fig = go.Figure(data=[go.Pie(
        labels=data['Symbol'], 
        values=[1]*len(data),
        hole=.7,
        marker_colors=colors,
        textinfo='label',
        hoverinfo='label+percent'
    )])
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text='MARKET<br>BREADTH', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig

# --- 2. Data Fetching Logic ---
nse_list = ["RELIANCE", "TCS", "HDFCBANK", "SBIN", "TATAMOTORS", "INFY", "ICICIBANK", "DLF", "GNFC", "HAL"]

def get_live_data(names):
    rows = []
    for t in names:
        try:
            stock = yf.Ticker(t + ".NS")
            df = stock.history(period="2d")
            if df.empty: continue
            cmp = round(df['Close'].iloc[-1], 2)
            open_p = df['Open'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            
            action = "BUY EXIT" if cmp > open_p else "SELL EXIT"
            trend = "Positive" if cmp > prev_close else "Negative"
            
            rows.append({
                "Action": action,
                "Symbol": t,
                "Entry": round(open_p, 2),
                "CMP": cmp,
                "Target": round(cmp * 1.015, 2) if action == "BUY EXIT" else round(cmp * 0.985, 2),
                "Financial Trend": trend,
                "Valuation": "Attractive" if trend == "Positive" else "Fair"
            })
        except: continue
    return pd.DataFrame(rows)

# --- 3. UI Layout ---
st.title("📟 Santosh Hybrid Terminal")
current_time = datetime.now().strftime("%H:%M:%S")
st.write(f"Auto-refreshing... Last update: {current_time}")

df_final = get_live_data(nse_list)

if not df_final.empty:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Index Mover Trend")
        st.plotly_chart(draw_circular_chart(df_final), use_container_width=True)
    
    with col2:
        st.subheader("Top Contributors")
        # List of top gainers/losers logic
        st.dataframe(df_final[['Symbol', 'CMP', 'Financial Trend']].sort_values(by='CMP', ascending=False), height=300)

    st.markdown("---")
    st.subheader("📊 Intraday Trade Guide (Motilal Style)")
    
    # Styling for the main table
    def style_final(val):
        if val == 'BUY EXIT': return 'background-color: #1b5e20; color: white;'
        if val == 'SELL EXIT': return 'background-color: #b71c1c; color: white;'
        return ''

    st.table(df_final.style.map(style_final, subset=['Action']))

# Auto Refresh logic
time.sleep(60)
st.rerun()
