"""Sidebar usada em todas as páginas do dashboard."""

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
    """Div para exibir os links para acessar as minhas informações específicas.

    Returns:
    html.Div: Div que contém os links de acesso a informações.
    """
    return html.Div(
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


def minhas_informacoes() -> html.Div:
    """Div para exibir as informações do usuário.

    Returns:
        html.Div: Div contendo o nome e os links de acesso a informações.
    """
    return html.Div(
        [
            html.H1("Fenyx Forte", className="meu-nome"),
            html.Hr(),
            links_minhas_informacoes(),
        ],
    )


def links_paginas() -> Nav:
    """Gera uma lista com links para diferentes páginas.

    Returns:
    Nav: Elemento HTML que contém a lista de links.
    """
    return Nav(
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


def links_documentacao() -> html.Div:
    """Div para exibir os links de documentação da aplicação.

    Returns:
        html.Div: Div contendo os links para a documentação.
    """
    return html.Div(
        [
            html.A(
                [
                    html.I(className="fa-solid fa-code"),
                    html.Label("Repositório"),
                ],
                href="https://github.com/Fenyx-Forte/Pesquisa-De-Mercado-Tenis-Corrida-Masculino",
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
                href="https://fenyx-forte.github.io/Pesquisa-De-Mercado-Tenis-Corrida-Masculino/",
                target="_blank",
                rel="noreferrer",
            ),
        ],
    )


def creditos_imagens_e_icones() -> html.Div:
    """Div para exibir informações sobre os créditos das imagens e ícones utilizados no dashboard.

    Returns:
        html.Div: Div contendo as informações sobre créditos.
    """
    return html.Div(
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


def sidebar() -> html.Div:
    """Barra lateral para navegar pelo dashboard e para exibir informações e links importantes.

    Returns:
        html.Div: Div representando a sidebar.
    """
    return html.Div(
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
