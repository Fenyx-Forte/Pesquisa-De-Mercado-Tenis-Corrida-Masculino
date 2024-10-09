from dash import html

from dashboard.processamento import gerenciador


def botao_toggle() -> html.Div:
    conteudo = html.Div(
        html.I(className="fas fa-bars"),
        className="meu-toggle-navbar",
        id="meu-toggle-navbar",
    )

    return conteudo


def titulo() -> html.H1:
    conteudo = html.H1(
        "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        className="text-primary text-center fs-3",
        id="titulo-aplicacao",
    )

    return conteudo


def informacao_data_coleta() -> html.H4:
    conteudo = html.H4(
        f"Data Coleta: {gerenciador.retorna_cabecalho_data_coleta()}",
        className="text-center",
        id="data-coleta",
    )

    return conteudo


def cabecalho() -> html.Div:
    conteudo = html.Div(
        [
            botao_toggle(),
            titulo(),
            informacao_data_coleta(),
        ],
        id="cabecalho",
    )

    return conteudo
