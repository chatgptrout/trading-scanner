def turbo_scan(sym):
    try:
        df = yf.download(sym, period='1d', interval='5m', progress=False)
        if not df.empty and len(df) > 5:
            rsi = ta.rsi(df['Close'], length=14).iloc[-1]
            price = df['Close'].iloc[-1]
            ema = ta.ema(df['Close'], length=20).iloc[-1]
            
            # Turbo Logic: Thoda sa bhi momentum aate hi signal dikhao
            if rsi > 50 and price > ema:
                return {'sym': sym, 'type': 'BUY', 'price': price, 'rsi': rsi}
            if rsi < 50 and price < ema:
                return {'sym': sym, 'type': 'SELL', 'price': price, 'rsi': rsi}
    except: return None
