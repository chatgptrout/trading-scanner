import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(layout="wide", page_title="Santosh Signal Pro")

# Professional UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .signal-card { 
        padding: 15px; border-radius: 8px; border: 1px solid #333; 
        text-align: center; margin-bottom: 10px; background-color: #111;
    }
    th { background-color: #1a1a1a !important; color: #ffca28 !important; }
    td { border: 0.1px solid #333 !important; padding: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic for Top Bar (Indices & Commodities)
def get_master_levels():
    tickers = {
        "NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN",
        "CRUDE OIL": "CL=F", "NAT GAS": "NG=F", "GOLD": "GC=F", "SILVER": "SI=F"
    }
    results = []
    for name, sym in tickers.items():
        try:
            data = yf.Ticker(sym).history(period="1d", interval="5m")
            if not data.empty:
                high, low = round(data['High'].max(), 2), round(data['Low'].min(), 2)
                cmp = data['Close'].iloc[-1]
                
                # Tradex Style: CMP decide karega signal kya hoga
                if cmp > (high + low)/2:
                    status, level, color = "BULLISH", f"ABOVE {high}", "#2ecc71"
                else:
                    status, level, color = "BEARISH", f"BELOW {low}", "#e74c3c"
                
                results.append({"name": name, "status": status, "level": level, "color": color})
        except: continue
    return results

# 3. Stock List (Nifty 50 + Bank Nifty Heavyweights)
stock_list = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "SBIN", "INFY", "TATAMOTORS", "AXISBANK", 
    "KOTAKBANK", "LT", "DLF", "GNFC", "HAL", "M&M", "BHARTIARTL", "ITC"
]

def get_stock_levels():
    rows = []
    data = yf.download([t + ".NS" for t in stock_list], period="1d", interval="5m", group_by='ticker', progress=False)
    for t in stock_list:
        try:
            df = data[t + ".NS"]
            if df.empty: continue
            high, low = round(df['High'].max(), 2), round(df['Low'].min(), 2)
            cmp = df['Close'].iloc[-1]
            
            # Level Logic
            if cmp > (high + low)/2:
                signal, level, color = "BULLISH", f"ABOVE {high}", "color: #2ecc71; font-weight: bold;"
            else:
                signal, level, color = "BEARISH", f"BELOW {low}", "color: #e74c3c; font-weight: bold;"
            
            rows.append({"Symbol": t, "CMP": round(cmp, 2), "Signal": signal, "Level": level, "Style": color})
        except: continue
    return pd.DataFrame(rows)

# --- DISPLAY ---
st.title("📟 Santosh Pro Master Signal Terminal")
st.write(f"Live Action Levels | Last Update: {datetime.now().strftime('%H:%M:%S')}")

# A. TOP SIGNALS (Indices & Commodities)
sigs = get_master_levels()
if sigs:
    cols = st.columns(len(sigs))
    for i, s in enumerate(sigs):
        with cols[i]:
            st.markdown(f"""
                <div class='signal-card'>
                    <small>{s['name']}</small>
                    <h3 style='color:{s['color']}; margin:5px 0;'>{s['status']}</h3>
                    <p style='margin:0; font-size:16px;'>{s['level']}</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# B. STOCK SIGNALS TABLE
df_stocks = get_stock_levels()
if not df_stocks.empty:
    st.subheader("📊 Equity & Bank Nifty Trade Signals")
    
    # Custom styling for the table rows
    def apply_signal_color(row):
        return [row['Style']] * len(row)

    # Display clean table with only levels
    display_df = df_stocks[['Symbol', 'CMP', 'Signal', 'Level']]
    st.table(display_df.style.apply(lambda x: [x.Style]*4 if x.Signal == 'BULLISH' else [x.Style]*4, axis=1))

# 4. AUTO REFRESH
time.sleep(60)
st.rerun()
