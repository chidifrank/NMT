import dash_bootstrap_components as dbc
import dash_html_components as html

nav_bar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.A(dbc.NavbarBrand("Machine translation | Dashboard", className="ml-2"), href='/')),
                ],
                align="center",
                no_gutters=True
            )
        )
    ],
    color="primary",
    dark=True,
    className='mr-auto'
)
