from dash import (
    Input,
    Output,
    clientside_callback,
    html,
)
from dash.dcc import Location
from dash_bootstrap_components import Nav, NavLink

from dashboard.uteis import uteis_processamento


def links_minhas_informacoes() -> html.Div:
    conteudo = html.Div(
        [
            html.A(
                [
                    html.Img(
                        src="/assets/images/portfolio.png",
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
                    html.I(className="fa-brands fa-linkedin-in"),
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
    )

    return conteudo


def minhas_informacoes() -> html.Div:
    conteudo = html.Div(
        [
            html.H1("Fenyx Forte", className="text-primary"),
            html.Hr(),
            links_minhas_informacoes(),
        ]
    )

    return conteudo


def links_paginas() -> Nav:
    conteudo = Nav(
        [
            NavLink(
                html.Div("Home"),
                href="/",
                active="exact",
            ),
            NavLink(
                html.Div("KPI's"),
                href="/kpis",
                active="exact",
            ),
            NavLink(
                html.Div("Top 10 Marcas Atuais"),
                href="/top-10-marcas-atuais",
                active="exact",
            ),
            NavLink(
                html.Div("Top 10 Marcas Período"),
                href="/top-10-marcas-periodo",
                active="exact",
            ),
            NavLink(
                html.Div("Preço Médio"),
                href="/preco-medio",
                active="exact",
            ),
            NavLink(
                html.Div("Faixa Preço"),
                href="/faixa-preco",
                active="exact",
            ),
            NavLink(
                html.Div("Satisfação"),
                href="/satisfacao",
                active="exact",
            ),
            NavLink(
                html.Div("Promoções"),
                href="/promocoes",
                active="exact",
            ),
        ],
        vertical=True,
        pills=True,
    )

    return conteudo


def links_documentacao() -> html.Div:
    conteudo = html.Div(
        [
            html.A(
                [
                    html.I(className="fa-solid fa-code"),
                    html.Label("Repositório"),
                ],
                href="https://github.com/Fenyx-Forte/Pesquisa-De-Mercado-Tenis-Corrida-Mercado-Livre",
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
                href="https://github.com/Fenyx-Forte/Pesquisa-De-Mercado-Tenis-Corrida-Mercado-Livre",
                target="_blank",
                rel="noreferrer",
            ),
        ],
    )

    return conteudo


def creditos_imagens_e_icones() -> html.Div:
    conteudo = html.Div(
        [
            html.Div(
                html.Label(
                    "Imagens e Ícones:",
                    className="label-creditos-titulo",
                ),
            ),
            html.A(
                html.Label(
                    "Freepik",
                    className="label-creditos",
                ),
                href="https://www.freepik.com/",
                target="_blank",
                rel="noreferrer",
            ),
            html.Br(),
            html.A(
                html.Label(
                    "Font Awesome Icons",
                    className="label-creditos",
                ),
                href="https://fontawesome.com/icons",
                target="_blank",
                rel="noreferrer",
            ),
        ],
    )

    return conteudo


def sidebar() -> html.Div:
    conteudo = html.Div(
        [
            Location(id="url-atual", refresh=False),
            html.Div(
                [
                    minhas_informacoes(),
                    html.Hr(),
                    links_paginas(),
                    html.Hr(),
                    links_documentacao(),
                    html.Hr(),
                    creditos_imagens_e_icones(),
                ],
            ),
        ],
        id="minha-sidebar",
        className="minha-sidebar",
    )

    return conteudo


clientside_callback(
    uteis_processamento.callback_atualizar_titulo_pagina(),
    Input("url-atual", "pathname"),
)

clientside_callback(
    uteis_processamento.callback_fechar_sidebar(),
    Output("coluna-sidebar", "class_name", allow_duplicate=True),
    Input("url-atual", "pathname"),
    prevent_initial_call=True,
)

clientside_callback(
    uteis_processamento.callback_abrir_e_fechar_sidebar(),
    Output("coluna-sidebar", "class_name", allow_duplicate=True),
    Input("meu-toggle-navbar", "n_clicks"),
    prevent_initial_call=True,
)
