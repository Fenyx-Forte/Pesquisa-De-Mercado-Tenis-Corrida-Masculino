from dash import html, page_registry
from dash_bootstrap_components import Nav, NavLink


def sidebar():
    sidebar = html.Div(
        [
            html.Br(),
            Nav(
                [
                    NavLink(
                        html.Div(page["name"]),
                        href=page["path"],
                        active="exact",
                    )
                    for page in page_registry.values()
                    if page["name"] != "Not Found 404"
                ],
                vertical=True,
                pills=True,
            ),
            html.Div(id="input-estatico"),
        ],
        className="sidebar",
    )

    return sidebar
