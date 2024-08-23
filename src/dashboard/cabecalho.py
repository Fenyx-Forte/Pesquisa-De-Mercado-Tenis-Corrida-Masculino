from dash import html


def cabecalho(data_coleta: str) -> html.Div:
    titulo_1 = html.H1(
        "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        className="text-primary text-center fs-3",
        id="titulo-aplicacao",
    )

    data_coleta_html = html.P(
        f"Data Coleta: {data_coleta}",
        className="text-center",
        id="data-coleta",
    )

    return html.Div(
        [titulo_1, data_coleta_html, html.Hr()], className="cabecalho"
    )
