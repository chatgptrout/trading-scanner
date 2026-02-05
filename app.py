import streamlit as st
import requests

st.title("SANTOSH SMART SCANNER")

token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {'access-token': token, 'Content-Type': 'application/json'}
        payload = {"instruments": [{"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX"}]}
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            price = data.get('data', {}).get('MCX:CRUDEOIL FEB FUT', 0)
            st.metric("CRUDE OIL PRICE", f"Rs {price}")
            st.success("LIVE MATCHED!")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Please Paste 'OfficeScanner' Token")
