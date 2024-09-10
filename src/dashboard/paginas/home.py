import plotly.express as px
from dash import Input, Output, State, callback, dcc, html, register_page
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import Button

from dashboard.processamento import gerenciador

register_page(
    __name__,
    path="/",
    name="Home",
    title="Home",
    description="Página Home",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Titulo Pagina")

    return conteudo


def seletor_datas() -> dcc.DatePickerRange:
    conteudo = dcc.DatePickerRange(
        id="seletor-datas",
        start_date_placeholder_text="Data Inicial",
        end_date_placeholder_text="Data Final",
        display_format="DD/MM/YYYY",
        min_date_allowed=gerenciador.retorna_data_coleta_mais_antiga(),
        max_date_allowed=gerenciador.retorna_data_coleta_mais_recente(),
        clearable=True,
        minimum_nights=0,
        show_outside_days=False,
    )

    return conteudo


def botao_adicionar_periodo() -> Button:
    conteudo = Button(
        "Adicionar Período",
        outline=True,
        color="primary",
        className="me-1",
        id="botao-adicionar-periodo",
    )

    return conteudo


def grafico_top_10_marcas() -> dcc.Graph:
    figura = px.bar(
        gerenciador.pagina_1_top_10_marcas_atual(),
        x="Marca",
        y="Porcentagem",
        color="Período",
        barmode="group",
    ).update_layout(dragmode=False)

    conteudo = dcc.Graph(
        figure=figura,
        config={
            "displayModeBar": False,
            "doubleClick": False,
            "editSelection": False,
            "editable": False,
            "scrollZoom": False,
            "showTips": False,
        },
        id="grafico-top-10-marcas",
    )

    return conteudo


layout = html.Div(
    [
        titulo(),
        html.Br(),
        seletor_datas(),
        html.Br(),
        html.Br(),
        botao_adicionar_periodo(),
        grafico_top_10_marcas(),
    ],
    className="pagina",
)


@callback(
    Output("grafico-top-10-marcas", "figure"),
    Output("seletor-datas", "start_date"),
    Output("seletor-datas", "end_date"),
    Input("botao-adicionar-periodo", "n_clicks"),
    State("seletor-datas", "start_date"),
    State("seletor-datas", "end_date"),
    State("grafico-top-10-marcas", "figure"),
    prevent_initial_call=True,
)
def adicionar_comparacao(n_clicks, data_inicio, data_fim, dados_grafico_atual):
    if data_inicio is None:
        raise PreventUpdate
    if data_fim is None:
        raise PreventUpdate

    qtd_periodos = len(dados_grafico_atual["data"])

    if qtd_periodos >= 3:
        raise PreventUpdate

    dados_grafico = gerenciador.pagina_1_grafico_comparacao_top_10(
        dados_grafico_atual, data_inicio, data_fim
    )

    figura_nova = px.bar(
        dados_grafico,
        x="Marca",
        y="Porcentagem",
        color="Período",
        barmode="group",
    ).update_layout(dragmode=False)

    return figura_nova, None, None
