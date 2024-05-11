import dash
from dash import dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template="/", name="Home")

def get_home_md():
    file = open('app/pages/home.md', 'r')
    raw = file.read()
    raw = raw.split("\n")
    new_raw = []
    for line in raw:
        # if not line.startswith("!["):
        new_raw.append(line)
    raw = "\n".join(new_raw)
    return raw

layout = dbc.Container(dcc.Markdown(get_home_md()), 
                       style={'padding':'30px'})