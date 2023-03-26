import dash
from dash import html
from dash import dcc
import subprocess

# Define the Bash script to run
bash_script = "/home/aki/ProjetLinux/scrap.sh"

# Run the Bash script and capture its output
result = subprocess.check_output(['bash', '-c', bash_script]).decode('utf-8')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Bash Script Output'),
    dcc.Textarea(
        value=result,
        readOnly=True,
        style={'width': '100%', 'height': 300}
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port = 8011)
