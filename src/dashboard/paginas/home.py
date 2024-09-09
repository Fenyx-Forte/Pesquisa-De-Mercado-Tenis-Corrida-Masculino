import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, Patch, State, callback, dcc, html, register_page
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import Button

from dashboard.uteis import processamento_dados

register_page(
    __name__,
    path="/",
    name="Home",
    title="Home",
    description="Página Home",
    image_url="/assets/images/imagem_link.jpg",
)


layout = html.Div(
    [
        dcc.DatePickerRange(
            id="intervalo-datas",
            start_date_placeholder_text="Data Inicial",
            end_date_placeholder_text="Data Final",
            display_format="DD/MM/YYYY",
            min_date_allowed=processamento_dados.retorna_dia_coleta_mais_antiga(),
            max_date_allowed=processamento_dados.retorna_dia_coleta_mais_recente(),
            clearable=True,
            minimum_nights=0,
            show_outside_days=False,
        ),
        html.Br(),
        html.Br(),
        Button(
            "Adicionar Período",
            outline=True,
            color="primary",
            className="me-1",
            id="botao-adicionar-periodo",
        ),
        dcc.Graph(
            figure=px.bar(
                processamento_dados.retorna_top_10_marcas_dados_mais_recentes(),
                x="Marca",
                y="Porcentagem",
                color="Período",
                barmode="group",
            ).update_layout(dragmode=False),
            config={
                "displayModeBar": False,
                "doubleClick": False,
                "editSelection": False,
                "editable": False,
                "scrollZoom": False,
                "showTips": False,
            },
            id="grafico-top-10-marcas",
        ),
    ],
    className="pagina",
)


@callback(
    Output("grafico-top-10-marcas", "figure"),
    Output("intervalo-datas", "start_date"),
    Output("intervalo-datas", "end_date"),
    Input("botao-adicionar-periodo", "n_clicks"),
    State("intervalo-datas", "start_date"),
    State("intervalo-datas", "end_date"),
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

    dados_grafico = processamento_dados.retorna_dados_grafico_comparacao_top_10(
        dados_grafico_atual, data_inicio, data_fim
    )

    figure = px.bar(
        dados_grafico,
        x="Marca",
        y="Porcentagem",
        color="Período",
        barmode="group",
    ).update_layout(dragmode=False)

    return figure, None, None
