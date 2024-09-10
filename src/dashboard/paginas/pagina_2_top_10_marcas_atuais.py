import plotly.express as px
from dash import Input, Output, State, callback, dcc, html, register_page
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import Button
from pandas import DataFrame as pd_DataFrame

from dashboard.processamento import gerenciador

register_page(
    __name__,
    path="/top-10-marcas-atuais",
    name="Top 10 Marcas Atuais",
    title="Top 10 Marcas Atuais",
    description="Top 10 Marcas Atuais",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Top 10 Marcas Atuais")

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


def figura_top_10_marcas(df: pd_DataFrame) -> px.bar:
    figura = (
        px.bar(
            df,
            x="Marca",
            y="Porcentagem",
            color="Período",
            color_discrete_sequence=["#6495ED", "#FFA07A", "#5CB85C"],
            barmode="group",
            hover_data={
                "Porcentagem": ":.2f",
                "Período": False,
                "Marca": False,
            },
            text_auto=".2f",
        )
        .update_traces(
            textfont_size=12,
            textangle=0,
            textfont_color="#000000",
            textposition="outside",
            cliponaxis=False,
            # textposition="auto",
        )
        .update_layout(
            dragmode=False,
            hoverlabel=dict(font_size=12, font_color="#FFFFFF"),
            uniformtext_minsize=10,
            uniformtext_mode="hide",
            legend=dict(
                font=dict(size=14, color="black"),
            ),
        )
    )

    return figura


def grafico_top_10_marcas() -> dcc.Graph:
    figura = figura_top_10_marcas(gerenciador.pagina_2_top_10_marcas_atuais())

    conteudo = dcc.Graph(
        figure=figura,
        responsive=True,
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
        # titulo(),
        # html.Br(),
        seletor_datas(),
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

    dados_grafico = gerenciador.pagina_2_grafico_comparacao_top_10(
        dados_grafico_atual, data_inicio, data_fim
    )

    figura_nova = figura_top_10_marcas(dados_grafico)

    return figura_nova, None, None
