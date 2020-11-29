import dash_html_components as html
import sys

# Setting relative path
sys.path.insert(0, "/var/www/FlaskApp/FlaskApp")

from app import app
from components.elements.nav_bar import nav_bar
from components.pages.home_page import page

# Our website layout with our nav_bar and page
app.layout = \
    html.Div(
        [
            nav_bar,
            page
        ],
        style={'width': '99%'},
    )

server = app.server

if __name__ == '__main__':
    # Run our server with debug mode on
    app.run_server(debug=True)
