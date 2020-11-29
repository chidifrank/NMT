import dash as dash
import dash_bootstrap_components as dbc
from flask import Flask

# Initialize our Flask server
server = Flask(__name__)

# Initialize our dash app with our flask server as backend
app = dash.Dash(server=server,
                update_title='Loading...',
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SANDSTONE])
app.title = 'Machine translation tool'
