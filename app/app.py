import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from updater.db_helpers import DB

def init_dash_app(server):
    app = dash.Dash(__name__, server=server, use_pages=True, url_base_pathname='/', \
            external_stylesheets=[dbc.themes.JOURNAL])

    available_pages = dash.page_registry.values()

    app.layout = html.Div(
        [
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="/")),
                    dbc.NavItem(dbc.NavLink("Prices", href="/prices")),
                    dbc.NavItem(dbc.NavLink("Archive", href="/archive")),
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
    return app