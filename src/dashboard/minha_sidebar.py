import dash_bootstrap_components as dbc
from dash import html


def sidebar():
    sidebar_style = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "12rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
        "box-shadow": "5px 5px 5px 5px lightgrey",
    }

    h1_style = {"font-size": "30px", "font-weight": "bold"}

    h2_style = {
        "font-size": "20px",
    }

    sidebar = html.Div(
        [
            html.H1("Sidebar", h1_style),
            html.Hr(),
            html.H2(
                "A simple sidebar layout with navigation links",
                className="lead",
                style=h2_style,
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Page 1", href="/page-1", active="exact"),
                    dbc.NavLink("Page 2", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=sidebar_style,
    )

    return sidebar
