"""Página Home."""

from dash import html, register_page
from dash_bootstrap_components import (
    Col,
    Row,
)

from dashboard.processamento import gerenciador
from dashboard.uteis import componentes_pagina

register_page(
    __name__,
    path="/",
    name="Home",
    title="Home",
    description="Página Home",
    image_url="https://analise-de-dados-tenis-corrida.onrender.com/assets/images/imagem_link.jpg",
)


def id_pagina() -> str:
    """Id da página.

    Returns:
        str: id da página.
    """
    return "home"


def titulo_pagina() -> str:
    """Título da página.

    Returns:
        str: Título da página.
    """
    return "Home"


def secao_contexto() -> html.Div:
    """Contexto do dashboard.

    Returns:
        html.Div: Contexto do dashboard.
    """
    periodo_coleta = gerenciador.retorna_periodo_historico()

    texto_contexto = """
        Os dados do dashboard são refentes ao resultado de pesquisar por
        "tenis-corrida-masculino" em uma grande plataforma de E-commerce. Mais precisamente,
        são os dados relativos às 10 primeiras páginas dessa pesquisa.
    """

    return html.Div(
        [
            html.H4("Contexto", className="titulo_um"),
            html.Div(texto_contexto),
            html.Div(
                f"Os dados foram coletados no período de {periodo_coleta}.",
            ),
            html.Div(
                "Os dados foram coletados diariamente por volta de 01:00 ou 02:30 da madrugada.",
            ),
        ],
        className="secao",
    )


def secao_foco() -> html.Div:
    """Detalha o foco do dashboard.

    Returns:
        html.Div: Foco do dashboard.
    """
    return html.Div(
        [
            html.H4("Foco"),
            html.Div(
                "O foco do dashboard é auxiliar a responder as seguintes perguntas:",
            ),
            html.Div(
                "1) Hoje é um dia bom para comprar?",
                className="perguntas",
            ),
            html.Div(
                "2) Como o dia de hoje se compara a outros dias ou a outros períodos?",
                className="perguntas",
            ),
            html.Div(
                "3) Quais são as marcas mais procuradas?",
                className="perguntas",
            ),
            html.Div(
                "4) Quais marcas têm preço médio inferior a R$200?",
                className="perguntas",
            ),
            html.Div(
                "5) Quais marcas têm preço médio entre R$200 e R$400?",
                className="perguntas",
            ),
            html.Div(
                "6) Quais marcas têm preço médio acima de R$400?",
                className="perguntas",
            ),
            html.Div(
                "7) Quais marcas são as mais bem avaliadas?",
                className="perguntas",
            ),
            html.Div(
                "8) Quais marcas têm o maior número de avaliações?",
                className="perguntas",
            ),
            html.Div(
                "9) Quais marcas oferecem mais promoções?",
                className="perguntas",
            ),
            html.Div(
                "10) Quais marcas oferecem os melhores descontos?",
                className="perguntas",
            ),
        ],
        className="secao",
    )


def secao_links() -> html.Div:
    """Todos os links relativos ao dashboard.

    Returns:
        html.Div: Seção de links.
    """
    return html.Div(
        [
            html.H4("Links"),
            html.Div(
                "(Para abrir o menu lateral, vá para o topo da página. Depois, clique no botão que está do lado esquerdo.)",
            ),
            html.Div(
                "Todos os links do dashboard se encontram no menu lateral.",
            ),
            html.Div("Minhas informações:", className="subsecao_links"),
            html.Div(
                [
                    html.A(
                        "Portfólio",
                        href="https://fenyx-forte.github.io/",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Meu portfólio.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "GitHub",
                        href="https://github.com/Fenyx-Forte",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Meu GitHub.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "Gmail",
                        href="mailto:fenyxforte@gmail.com",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Meu email.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                "Páginas do dashboard:",
                className="subsecao_links",
            ),
            html.Div(
                [
                    html.A(
                        "Home",
                        href="/",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Página inicial.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "KPI's",
                        href="/kpis",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        'Principais indicadores para a pergunta "Hoje é um dia bom para comprar?".',
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "Top 10 Marcas Atuais",
                        href="/top-10-marcas-atuais",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Como as 10 marcas mais procuradas de hoje estavam em outros períodos?",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "Top 10 Marcas Período",
                        href="/top-10-marcas-periodo",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Quais são as 10 marcas mais procuradas de cada período?",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "Preço Médio",
                        href="/preco-medio",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Preço médio por marca.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "Faixa Preço",
                        href="/faixa-preco",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Faixa de preço por marca.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "Satisfação",
                        href="/satisfacao",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Satisfação por marca.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "Promoções",
                        href="/promocoes",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Promoções por marca.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                "Documentação:",
                className="subsecao_links",
            ),
            html.Div(
                [
                    html.A(
                        "Repositório",
                        href="https://github.com/Fenyx-Forte/Pesquisa-De-Mercado-Tenis-Corrida-Masculino",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Repositório do projeto.",
                        className="resumo_link",
                    ),
                ],
            ),
            html.Div(
                [
                    html.A(
                        "Documentação",
                        href="https://fenyx-forte.github.io/Pesquisa-De-Mercado-Tenis-Corrida-Masculino/",
                        target="_blank",
                        rel="noreferrer",
                        className="links_na_sidebar",
                    ),
                    html.Div(
                        "Documentação do projeto.",
                        className="resumo_link",
                    ),
                ],
            ),
        ],
        className="secao",
    )


def coluna() -> html.Div:
    """Conteúdo de uma coluna.

    Returns:
        html.Div: Coluna.
    """
    return html.Div(
        [
            secao_contexto(),
            secao_foco(),
            secao_links(),
        ],
    )


def colunas() -> Row:
    """Colunas que compoem o conteúdo da página.

    Returns:
        Row: Conjunto de colunas.
    """
    return Row(
        [
            Col(
                coluna(),
                xs=12,
                class_name="coluna_home",
            ),
        ],
    )


layout = html.Div(
    [
        componentes_pagina.div_titulo(titulo_pagina()),
        colunas(),
    ],
    className="pagina",
    id=id_pagina(),
)
