from dash import html, page_registry
from dash_bootstrap_components import Nav, NavbarBrand, NavLink


def sidebar():
    sidebar = html.Div(
        [
            html.Div(
                [
                    html.H1("Fenyx Forte"),
                    html.Hr(),
                    html.Div(
                        [
                            html.A(
                                [
                                    html.Img(
                                        src="assets/favicon.ico",
                                        className="meu-icone",
                                    ),
                                    html.Label("Portfólio"),
                                ],
                                href="https://fenyx-forte.github.io/",
                                target="_blank",
                                rel="noreferrer",
                            ),
                            html.Br(),
                            html.A(
                                [
                                    html.I(
                                        className="fa-brands fa-linkedin-in"
                                    ),
                                    html.Label("Linkedin"),
                                ],
                                href="https://www.linkedin.com/in/fenyxforte/",
                                target="_blank",
                                rel="noreferrer",
                            ),
                            html.Br(),
                            html.A(
                                [
                                    html.I(className="fa-brands fa-github"),
                                    html.Label("GitHub"),
                                ],
                                href="https://github.com/Fenyx-Forte",
                                target="_blank",
                                rel="noreferrer",
                            ),
                            html.Br(),
                            html.A(
                                [
                                    html.I(className="fa-brands fa-google"),
                                    html.Label("Gmail"),
                                ],
                                href="mailto:fenyxforte@gmail.com",
                                target="_blank",
                                rel="noreferrer",
                            ),
                        ],
                        className="minha-sidebar-links",
                    ),
                ]
            ),
            html.Hr(),
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
        className="minha-sidebar",
    )

    return sidebar
