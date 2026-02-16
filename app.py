import streamlit as st
import pandas as pd
import time

# --- PC WHITE PRO THEME ---
st.set_page_config(page_title="SANTOSH SNIPER PC", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .breakout-card { 
        background: #ffffff; border: 1px solid #e1e4e8; border-radius: 15px; 
        padding: 25px; margin-bottom: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }
    .buy-zone { border-left: 12px solid #28a745; background-color: #f0fff4; }
    .sell-zone { border-left: 12px solid #dc3545; background-color: #fff5f5; }
    .price-big { font-size: 35px; font-weight: bold; color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

# Aapka Final CSV Link (Stocks & Commodity)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def fetch_active_trades():
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = df.columns.str.strip()
        # Cleaning data: Sirf Bullish/Bearish/Positional/Shorts filter honge
        df['Status'] = df['Signal Type'].astype(str).str.strip().str.upper()
        active = df[df['Status'].isin(['BULLISH', 'BEARISH', 'POSITIONAL', 'SHORTS'])]
        return active
    except:
        return pd.DataFrame()

st.markdown("<h1 style='text-align: center;'>🎯 LIVE BREAKOUT TERMINAL</h1>", unsafe_allow_html=True)

active_df = fetch_active_trades()

if not active_df.empty:
    # PC ki badi screen par 2 bade columns
    c1, c2 = st.columns(2)
    for i, (idx, row) in enumerate(active_df.iterrows()):
        target_col = c1 if i % 2 == 0 else c2
        
        # Bullish vs Bearish logic
        is_up = row['Status'] in ['BULLISH', 'POSITIONAL']
        style = "buy-zone" if is_up else "sell-zone"
        label = "🟢 BUY BREAKOUT" if is_up else "🔴 SELL BREAKOUT"
        l_color = "#28a745" if is_up else "#dc3545"
        
        with target_col:
            st.markdown(f"""
                <div class="breakout-card {style}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 28px; font-weight: bold;">{row['Symbol']}</span>
                        <span style="color: {l_color}; font-weight: bold; font-size: 18px;">{label}</span>
                    </div>
                    <hr style="border: 0.5px solid #eee; margin: 20px 0;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div style="color: #888; font-size: 16px;">LIVE LTP</div>
                        <div class="price-big">₹{row['LTP']}</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; text-align: center;">
                        <div style="background:#fff; padding:12px; border-radius:10px; border:1px solid #f1f1f1;">
                            <small style="color:#666;">ENTRY (High)</small><br><b style="font-size:18px;">{row['High']}</b>
                        </div>
                        <div style="background:#fff; padding:12px; border-radius:10px; border:1px solid #f1f1f1;">
                            <small style="color:#666;">STOP LOSS</small><br><b style="color:#dc3545; font-size:18px;">{row['Stop Loss']}</b>
                        </div>
                        <div style="background:#fff; padding:12px; border-radius:10px; border:1px solid #f1f1f1;">
                            <small style="color:#666;">TARGET</small><br><b style="color:#007bff; font-size:18px;">{row['Target']}</b>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # Screen khali dikhayega jab tak breakout na ho
    st.markdown("""
        <div style="text-align: center; margin-top: 100px; color: #adb5bd;">
            <h2 style="font-size: 50px;">⌛</h2>
            <h3>No Live Breakouts Detected</h3>
            <p>Waiting for 'BULLISH' or 'BEARISH' signals in Santosh Multi-Scanner...</p>
        </div>
    """, unsafe_allow_html=True)

time.sleep(5)
st.rerun()
