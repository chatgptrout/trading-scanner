# Stock List logic add kar diya hai
st.subheader("🚀 Rocket Breakout Stocks")
stock_col1, stock_col2 = st.columns(2)
with stock_col1:
    st.success("✅ RELIANCE - Buy Above 2950")
    st.success("✅ HDFC BANK - Buy Above 1680")
with stock_col2:
    st.error("🛑 SBI - Sell Below 720")
