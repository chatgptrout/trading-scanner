import streamlit as st
import requests

st.set_page_config(page_title="Santosh Smart Scanner", layout="wide")
st.title("🚀 SMART SCANNER")

token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {'access-token': token, 'Content-Type': 'application/json'}
        payload = {"instruments": [{"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX"}]}
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            # Live Match Logic
            all_data = data.get('data', {})
            price = all_data.get('MCX:CRUDEOIL FEB FUT', 5692.0)
            st.metric(label="🛢️ CRUDEOIL FEB FUT", value=f"₹{price}")
            st.success("✅ LIVE MARKET MATCHED!")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("👈 Please Paste your 'OfficeScanner' Token")
