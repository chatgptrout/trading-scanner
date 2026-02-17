import dash
from dash import html
import os

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("🚀 SANTOSH AI TERMINAL - LIVE", style={'textAlign': 'center', 'color': '#00FFCC'}),
    html.Div([
        html.H3("Market Monitoring Active", style={'color': '#FFCC00'}),
        html.P("Crude Oil: Tracking...", style={'fontSize': '20px'}),
        html.P("Nifty: Tracking...", style={'fontSize': '20px'})
    ], style={'textAlign': 'center', 'marginTop': '100px'})
], style={'backgroundColor': '#121212', 'height': '100vh', 'color': 'white'})

if __name__ == '__main__':
    # Render ke liye default settings
    app.run_server(debug=False)
