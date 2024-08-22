import dash
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
        "backgroundColor": "#f8f9fa",
        "boxShadow": "5px 5px 5px 5px lightgrey",
    }

    h1_style = {"fontSize": "30px", "fontWeight": "bold"}

    h2_style = {
        "fontSize": "16px",
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
                    dbc.NavLink(
                        html.Div(page["name"]),
                        href=page["path"],
                        active="exact",
                    )
                    for page in dash.page_registry.values()
                    if page["name"] != "Not Found 404"
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=sidebar_style,
    )

    return sidebar
