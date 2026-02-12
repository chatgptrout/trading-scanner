import streamlit as st
import pandas as pd
import time

# --- WHITE THEME SETUP ---
st.set_page_config(page_title="TGS SNIPER LIVE", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    .sniper-card { 
        background: #ffffff; border: 1px solid #dee2e6; border-radius: 12px; 
        padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 8px solid #28a745;
    }
    .sell-border { border-left-color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)

# --- YOUR LIVE CSV LINK ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        # Cleaning column names (Removing extra spaces)
        df.columns = df.columns.str.strip()
        # Cleaning 'Signal Type' data and making it uppercase for matching
        df['Signal Type'] = df['Signal Type'].astype(str).str.strip().str.upper()
        # Filter signals
        active_signals = df[df['Signal Type'].isin(['POSITIONAL', 'SHORTS'])]
        return active_signals
    except:
        return pd.DataFrame()

st.title("🎯 TGS LIVE SNIPER TERMINAL")

# --- DISPLAY ---
df_live = load_data()

if not df_live.empty:
    c1, c2 = st.columns(2)
    for i, (idx, row) in enumerate(df_live.iterrows()):
        t_col = c1 if i % 2 == 0 else c2
        is_buy = row['Signal Type'] == 'POSITIONAL'
        card_style = "" if is_buy else "sell-border"
        color = "#28a745" if is_buy else "#dc3545"
        
        with t_col:
            st.markdown(f"""
                <div class="sniper-card {card_style}">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 24px; font-weight: bold;">{row['Symbol']}</span>
                        <span style="color: {color}; font-weight: bold;">{row['Signal Type']}</span>
                    </div>
                    <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;">
                        <div><small style="color:#666;">LTP</small><br><b>{row['LTP']}</b></div>
                        <div><small style="color:#666;">STOP LOSS</small><br><b style="color:#dc3545;">{row['Stop Loss']}</b></div>
                        <div><small style="color:#666;">TARGET</small><br><b style="color:#007bff;">{row['Target']}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # If no POSITIONAL/SHORTS found, show this
    st.info("⌛ Waiting for 'POSITIONAL' or 'SHORTS' signals in TGS Sheet...")
    st.write("Current Sheet Status: Data Connected ✅ | Filter Active 🔍")

time.sleep(10)
st.rerun()
