import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = dash.Dash(use_pages=True,external_stylesheets=[dbc.themes.JOURNAL])


available_pages = dash.page_registry.values()

app.layout = html.Div(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Prices", href="/prices")),
                dbc.NavItem(dbc.NavLink("archive", href="/archive")),
            ],
            brand=html.Img(
                src="/assets/favicon.ico",
                height=70,
            ),
            brand_href="/",
            color='#90b4ce',
            # light=True,

        ),
        dash.page_container,
    ]
)

server = app.server

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5578)