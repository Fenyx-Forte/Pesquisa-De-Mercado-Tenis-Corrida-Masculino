"""Cabeçalho usado em todas as páginas do dashboard."""

from dash import html

from dashboard.processamento import gerenciador


def botao_toggle() -> html.Div:
    """Retorna um botão toggle.

    Returns:
        html.Div: Div que representa o botão toggle.
    """
    return html.Div(
        html.I(className="fas fa-bars"),
        className="meu-toggle-navbar",
        id="meu-toggle-navbar",
    )


def titulo() -> html.H1:
    """Retorna o título do cabeçalho.

    Returns:
        html.H1: H1 que representa o título do cabeçalho.
    """
    return html.H1(
        "Pesquisa de Mercado: Tênis de Corrida Masculino",
        className="text-primary text-center fs-3",
        id="titulo-aplicacao",
    )


def informacao_data_coleta() -> html.H4:
    """Retorna a última data de coleta dos dados.

    Returns:
        html.H4: H4 contendo a data de coleta.
    """
    return html.H4(
        f"Data Coleta: {gerenciador.retorna_cabecalho_data_coleta()}",
        className="text-center",
        id="data-coleta",
    )


def cabecalho() -> html.Div:
    """Gera um cabeçalho com o título, data de coleta e um botão.

    Returns:
        html.Div: Div representando o cabeçalho.
    """
    return html.Div(
        [
            botao_toggle(),
            titulo(),
            informacao_data_coleta(),
        ],
        id="cabecalho",
    )
