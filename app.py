import streamlit as st
import pandas as pd
import time

# --- PC OPTIMIZED WHITE THEME ---
st.set_page_config(page_title="SANTOSH BREAKOUT SNIPER", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .breakout-card { 
        background: #ffffff; border: 1px solid #e1e4e8; border-radius: 12px; 
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .bullish-bg { border-left: 10px solid #28a745; background-color: #f0fff4; }
    .bearish-bg { border-left: 10px solid #dc3545; background-color: #fff5f5; }
    .price-text { font-size: 28px; font-weight: bold; color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

# Aapki Commodity/Stock Sheet ka Link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def load_breakouts():
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = df.columns.str.strip()
        # Filter: Sirf Bullish ya Bearish dikhayega, 'Wait' ko filter kar dega
        df['Signal'] = df['Signal Type'].astype(str).str.upper()
        df = df[df['Signal'].isin(['BULLISH', 'BEARISH', 'POSITIONAL', 'SHORTS'])]
        return df
    except:
        return pd.DataFrame()

st.markdown("<h1 style='text-align: center;'>🎯 LIVE BREAKOUT SNIPER</h1>", unsafe_allow_html=True)

df_live = load_breakouts()

if not df_live.empty:
    # 2 columns mein breakouts dikhayega
    col1, col2 = st.columns(2)
    for i, (idx, row) in enumerate(df_live.iterrows()):
        t_col = col1 if i % 2 == 0 else col2
        
        is_bull = row['Signal'] in ['BULLISH', 'POSITIONAL']
        card_class = "bullish-bg" if is_bull else "bearish-bg"
        sig_color = "#28a745" if is_bull else "#dc3545"
        label = "BUY / BULLISH" if is_bull else "SELL / BEARISH"
        
        with t_col:
            st.markdown(f"""
                <div class="breakout-card {card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 24px; font-weight: bold;">{row['Symbol']}</span>
                        <span style="color: {sig_color}; font-weight: bold;">{label}</span>
                    </div>
                    <hr style="border: 0.5px solid #ddd; margin: 15px 0;">
                    <div style="text-align: center; margin-bottom: 15px;">
                        <div style="color: #666; font-size: 14px;">LIVE PRICE (LTP)</div>
                        <div class="price-text">₹{row['LTP']}</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;">
                        <div style="background:#fff; padding:8px; border-radius:8px;">
                            <small>ENTRY</small><br><b>{row['High']}</b>
                        </div>
                        <div style="background:#fff; padding:8px; border-radius:8px;">
                            <small>STOP LOSS</small><br><b style="color:#dc3545;">{row['Stop Loss']}</b>
                        </div>
                        <div style="background:#fff; padding:8px; border-radius:8px;">
                            <small>TARGET</small><br><b style="color:#007bff;">{row['Target']}</b>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # Screen khali hai matlab abhi market mein koi breakout nahi hai
    st.info("⌛ No Live Breakouts detected. Waiting for 'BULLISH' or 'BEARISH' signals in your sheet...")

time.sleep(5)
st.rerun()
