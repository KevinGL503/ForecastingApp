import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

available_pages = dash.page_registry.values()

app.layout = html.Div(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Data", href="/data")),
                dbc.NavItem(dbc.NavLink("archive", href="/archive")),
            ],
            brand=html.Img(
                src="/assets/favicon.ico",
                height=64,
            ),
            brand_href="/",
            color='blue',
            dark=True,
            className="mb-3",
        ),
        dash.page_container,
    ]
)

server = app.server

if __name__ == "__main__":
    app.run(debug=True, host='euclid.local',port=5578)