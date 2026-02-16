import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime
import os

# App Initialization
app = dash.Dash(__name__)
server = app.server 

# Layout: No Charts, Only Signals (As per your request)
app.layout = html.Div([
    html.H1("🚀 SANTOSH AI TERMINAL", style={'textAlign': 'center', 'color': '#00FFCC'}),
    html.Div(id='live-update-text', style={'fontSize': '24px', 'textAlign': 'center', 'marginTop': '50px'}),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
], style={'backgroundColor': '#121212', 'height': '100vh', 'color': 'white', 'padding': '20px'})

@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_signal(n):
    now = datetime.now().strftime("%H:%M:%S")
    return html.Div([
        html.P(f"Last Update: {now}"),
        html.H2("STATUS: MONITORING MARKET...", style={'color': '#FFCC00'}),
        html.P("CRUDE OIL: WAITING FOR BREAKOUT", style={'fontSize': '20px'})
    ])

if __name__ == '__main__':
    # Port 10000 Render ke liye sabse best hai
    app.run_server(host='0.0.0.0', port=10000, debug=False)
