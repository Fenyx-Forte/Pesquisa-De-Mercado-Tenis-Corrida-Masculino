import dash
import dash_bootstrap_components as dbc
from dash import html


def sidebar():
    sidebar = html.Div(
        [
            html.H1("Sidebar"),
            html.Br(),
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
        className="sidebar",
    )

    return sidebar
