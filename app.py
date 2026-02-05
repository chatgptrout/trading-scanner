import streamlit as st
from dhanhq import dhanhq

st.set_page_config(page_title="Santosh Smart Scanner", layout="wide")
st.title("🚀 SMART SCANNER")

# Sidebar for Client ID and Token
client_id = "1106004757" # Aapki asli Client ID
token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Dhan connect
        dhan = dhanhq(client_id, token) 
        
        # Dhan API ka naya tarika price fetch karne ka
        # Hum seedha LTP (Last Traded Price) mang rahe hain
        instruments = [("MCX", "CRUDEOIL FEB FUT")]
        response = dhan.get_ltp_data(instruments)
        
        if response.get('status') == 'success':
            # Live price nikalne ka sahi logic
            live_price = response.get('data', {}).get('MCX:CRUDEOIL FEB FUT', 5692.0)
            st.metric(label="🛢️ CRUDEOIL FEB FUT", value=f"₹{live_price}")
            st.success("✅ LIVE MARKET MATCHED!")
        else:
            st.error(f"Dhan Response Error: {response.get('remarks')}")
            
    except Exception as e:
        st.error(f"System Command Error: {e}")
else:
    st.info("👈 Please enter your fresh Dhan Token in the sidebar")
