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

def scrapBTC():
    bash_script = "/home/aki/ProjetLinux/scrap.sh"
    return subprocess.check_output(['bash', '-c', bash_script]).decode('utf-8')

def append_to_csv(result):
    with open("/home/aki/ProjetLinux/bitcoin_data.csv", 'a', newline = '') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(result)

def get_daily_report():
    df = pd.read_csv('bitcoin_data.csv', names=['Timestamp', 'Price'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.set_index('Timestamp').resample('D').agg({'Price': ['first', 'last', 'max', 'min']})
    df.columns = ['Open', 'Close', 'High', 'Low']
    df['Change'] = df['Close'] - df['Open']
    df['Volatility'] = df['High'] - df['Low']
    return df.tail(1)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Bitcoin Dashboard"),

    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(id='graph-update', interval=5*60*1000), # update every 5 minutes

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

@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph(n):
    try:
        df = pd.read_csv('bitcoin_data.csv', names=['Timestamp', 'Price'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

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
    except Exception as e:
        print(f"Error in update_graph: {e}")
        return dash.no_update




@app.callback(Output('daily-report', 'children'), [Input('daily-report-update', 'n_intervals')])
def update_daily_report(n):
    try:
        daily_report = get_daily_report()
        table = dash_table.DataTable(
            id='daily-report-table',
            columns=[{"name": i, "id": i} for i in daily_report.columns],
            data=daily_report.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
        return table
    except Exception as e:
        print(f"Error in update_daily_report: {e}")
        return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True, port=8011)
    while(True):
        result = scrapBTC()
        append_to_csv(result)
	
