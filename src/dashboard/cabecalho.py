import dash_bootstrap_components as dbc
from dash import Input, Output, callback, html


def cabecalho() -> html.Div:
    titulo_1 = html.H1(
        "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        className="text-primary text-center fs-3",
    )

    data_coleta_html = html.P(
        "",
        className="text-center",
        id="data_coleta",
    )

    return html.Div(
        [titulo_1, data_coleta_html, html.Hr()], className="cabecalho"
    )


@callback(
    Output(component_id="data_coleta", component_property="children"),
    Input(component_id="store", component_property="data"),
)
def preencher_data_coleta(store):
    return f"Data Coleta: {store["data_e_horario"]}"
