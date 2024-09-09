from dash import (
    Input,
    Output,
    clientside_callback,
    html,
    page_registry,
)
from dash_bootstrap_components import Nav, NavLink


def sidebar() -> html.Div:
    conteudo = html.Div(
        [
            html.Div(
                html.I(className="fas fa-bars"),
                className="meu-toggle-navbar",
                id="meu-toggle-navbar",
            ),
            html.Div(
                [
                    html.H1("Fenyx Forte", className="text-primary"),
                    html.Hr(),
                    html.Div(
                        [
                            html.A(
                                [
                                    html.Img(
                                        src="/assets/images/portfolio.ico",
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
                    html.Hr(),
                    html.Div(
                        [
                            html.A(
                                [
                                    html.I(className="fa-solid fa-code"),
                                    html.Label("Repositório"),
                                ],
                                href="https://github.com/Fenyx-Forte/Analise-De-Dados",
                                target="_blank",
                                rel="noreferrer",
                            ),
                            html.Br(),
                            html.A(
                                [
                                    html.I(className="fa-solid fa-book"),
                                    html.Label(
                                        "Documentação",
                                        className="label-documentacao",
                                    ),
                                ],
                                href="https://github.com/Fenyx-Forte",
                                target="_blank",
                                rel="noreferrer",
                            ),
                        ],
                    ),
                ],
            ),
        ],
        id="minha-sidebar",
        className="minha-sidebar",
    )

    return conteudo


clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks % 2 == 1) {
            return "minha-sidebar-escondida"
        }
        else {
            return "minha-sidebar"
        }
    }
    """,
    Output("minha-sidebar", "className"),
    Input("meu-toggle-navbar", "n_clicks"),
    prevent_initial_call=True,
)
