import yfinance as yf
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#121212', 'color': 'white', 'fontFamily': 'Arial', 'padding': '15px'}, children=[
    html.H1("🚀 SANTOSH AI TERMINAL", style={'textAlign': 'center', 'color': '#00FFCC'}),
    html.Div([
        dcc.Input(id='stock-input', value='RELIANCE.NS', type='text', style={'padding': '10px', 'borderRadius': '5px', 'width': '200px'}),
    ], style={'textAlign': 'center', 'marginBottom': '15px'}),
    html.Div(id='signal-box', style={'textAlign': 'center', 'fontSize': '35px', 'padding': '20px', 'borderRadius': '15px', 'margin': '10px'}),
    dcc.Graph(id='live-chart', style={'height': '60vh'}),
    dcc.Interval(id='timer', interval=15*1000, n_intervals=0)
])

@app.callback(
    [Output('live-chart', 'figure'), Output('signal-box', 'children'), Output('signal-box', 'style')],
    [Input('timer', 'n_intervals'), Input('stock-input', 'value')]
)
def update_app(n, ticker):
    try:
        df = yf.download(ticker, period='1d', interval='1m')
        if df.empty: return go.Figure(), "No Data Found", {}
        cp = df['Close'].iloc[-1]
        h15 = df['High'].iloc[-16:-1].max()
        if cp > h15:
            msg = f"🟢 BUY SIGNAL @ {cp:.2f}"
            style = {'backgroundColor': '#004d00', 'color': '#00FF00', 'border': '2px solid #00FF00'}
        else:
            msg = f"🟡 MONITORING @ {cp:.2f}"
            style = {'backgroundColor': '#333300', 'color': '#FFCC00', 'border': '2px solid #FFCC00'}
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=10, b=10))
        return fig, msg, style
    except:
        return go.Figure(), "Check Symbol Name", {}

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
