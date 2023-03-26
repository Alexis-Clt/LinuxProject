import dash
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import csv
import time
import subprocess

def scrapBTC():
    bash_script = "/home/aki/ProjetLinux/scrap.sh"
    return subprocess.check_output(['bash', '-c', bash_script]).decode('utf-8')

def append_to_csv(result):
    with open("/home/aki/ProjetLinux/bitcoin_data.csv", 'a', newline = '') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(result)

def update_graph():
    df = pd.read_csv('bitcoin_data.csv', names=['Price'])
    timestamps = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
    df['Timestamp'] = timestamps

    return {
        'data': [
            {'x': df['Timestamp'], 'y': df['Price'], 'type': 'line', 'name': 'Price'}
        ],
        'layout': {
            'title': 'Bitcoin Price Over Time',
            'xaxis': {'title': 'Timestamp'},
            'yaxis': {'title': 'Price'},
        }
    }

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Bitcoin Dashboard"),

    dcc.Graph(id='live-graph', animate=True, figure=update_graph()),
    dcc.Interval(id='graph-update', interval=1000), # update every 5 minutes

    html.H2("Daily Report"),
    html.Div(id="daily-report"),
    dcc.Interval(id="daily-report-update", interval=60*60*1000), # update every hour

    # Additional features and components can be added here
    dbc.Row([
        dbc.Col([
            html.Label("Select Cryptocurrency"),
            dcc.Dropdown(
                id="cryptocurrency-selector",
                options=[
                    {"label": "Bitcoin", "value": "bitcoin"},
                    {"label": "Ethereum", "value": "ethereum"},
                    # Add more options here
                ],
                value="bitcoin"
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8011)
    while(True):
        result = scrapBTC()
        append_to_csv(result)
        update_graph()
        time.sleep(5)
        
