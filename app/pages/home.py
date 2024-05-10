import dash
from dash import dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template="/", name="Home")


def get_readme_from_github():
    import requests

    url = "https://github.com/KevinGL503/ForecastingApp/raw/main/README.md"
    response = requests.get(url)

    raw = response.text
    raw = raw.split("\n")
    new_raw = []
    for line in raw:
        if not line.startswith("!["):
            new_raw.append(line)
    raw = "\n".join(new_raw)

    return raw


def layout():
    return dbc.Container([dbc.Card(dcc.Markdown(get_readme_from_github()), body=True)])