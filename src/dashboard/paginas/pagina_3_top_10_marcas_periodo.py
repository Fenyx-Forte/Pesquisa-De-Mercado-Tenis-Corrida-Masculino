import plotly.express as px
from dash import (
    Input,
    Output,
    Patch,
    State,
    callback,
    clientside_callback,
    dcc,
    html,
    register_page,
)
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import (
    Button,
    Col,
    Modal,
    ModalBody,
    ModalHeader,
    ModalTitle,
    Row,
)
from pandas import DataFrame as pd_DataFrame
from plotly.graph_objects import Figure

from dashboard.processamento import gerenciador
from dashboard.processamento.paginas import processamento_pagina_3

register_page(
    __name__,
    path="/top-10-marcas-periodo",
    name="Top 10 Marcas Período",
    title="Top 10 Marcas Período",
    description="Top 10 Marcas Período",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Top 10 Marcas Período")

    return conteudo


def seletor_datas() -> dcc.DatePickerRange:
    conteudo = dcc.DatePickerRange(
        id="pagina_3_seletor_datas",
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


def botao_selecionar_periodo() -> Button:
    conteudo = Button(
        "Selecionar Período",
        outline=True,
        color="primary",
        className="me-1",
        id="pagina_3_botao",
        class_name="botao",
    )

    return conteudo


def div_seletor_datas_e_botao() -> html.Div:
    conteudo = html.Div(
        [
            seletor_datas(),
            html.Br(),
            botao_selecionar_periodo(),
        ],
        className="div_seletor_datas_e_botao",
    )

    return conteudo


def modal_erro() -> Modal:
    conteudo = Modal(
        [
            ModalHeader(ModalTitle("Titulo", id="pagina_3_modal_erro_titulo")),
            ModalBody("Conteudo", id="pagina_3_modal_erro_conteudo"),
        ],
        id="pagina_3_modal_erro",
        is_open=False,
    )

    return conteudo


def figura_top_10_marcas(df: pd_DataFrame, cor: str) -> Figure:
    figura = (
        px.bar(
            df,
            x="Marca",
            y="Porcentagem",
            labels={
                "Porcentagem": "Porcentagem (%)",
            },
            color_discrete_sequence=[cor],
            barmode="group",
            hover_data={
                "Porcentagem": ":.2f",
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
            uniformtext_mode="show",
            showlegend=False,
        )
    )

    return figura


def grafico_top_10_marcas(df: pd_DataFrame, cor: str, sufixo: str) -> dcc.Graph:
    figura = figura_top_10_marcas(df=df, cor=cor)

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
        id=f"pagina_3_grafico_top_10_marcas_{sufixo}",
    )

    return conteudo


def div_periodo(
    titulo: str, periodo: str, df: pd_DataFrame, cor: str, sufixo: str
) -> html.Div:
    conteudo = html.Div(
        [
            html.H4(titulo, className="titulo_coluna"),
            html.Br(),
            html.Div(
                periodo,
                className="periodo_coluna",
                id=f"pagina_3_periodo_{sufixo}",
            ),
            html.Br(),
            grafico_top_10_marcas(df, cor, sufixo),
        ]
    )

    return conteudo


def colunas(
    periodo_hoje: str,
    periodo_escolhido: str,
    periodo_historico: str,
    df_hoje: pd_DataFrame,
    df_escolhido: pd_DataFrame,
    df_historico: pd_DataFrame,
) -> Row:
    conteudo = Row(
        [
            Col(
                div_periodo(
                    titulo="Hoje",
                    periodo=periodo_hoje,
                    df=df_hoje,
                    cor="#6495ED",
                    sufixo="hoje",
                ),
                width=4,
                class_name="coluna_hoje",
            ),
            Col(
                div_periodo(
                    titulo="Período Escolhido",
                    periodo=periodo_escolhido,
                    df=df_escolhido,
                    cor="#FFA07A",
                    sufixo="escolhido",
                ),
                width=4,
                class_name="coluna_escolhido",
            ),
            Col(
                div_periodo(
                    titulo="Histórico",
                    periodo=periodo_historico,
                    df=df_historico,
                    cor="#5CB85C",
                    sufixo="historico",
                ),
                width=4,
                class_name="coluna_historico",
            ),
        ],
        class_name="linha_colunas_periodos",
    )

    return conteudo


layout = html.Div(
    [
        # titulo(),
        # html.Br(),
        div_seletor_datas_e_botao(),
        modal_erro(),
        colunas(
            periodo_hoje=gerenciador.retorna_periodo_hoje(),
            periodo_escolhido=gerenciador.retorna_periodo_ultima_semana(),
            periodo_historico=gerenciador.retorna_periodo_historico(),
            df_hoje=gerenciador.retorna_top_10_marcas_hoje(),
            df_escolhido=gerenciador.pagina_3_inicializa_top_10_marcas_escolhido(),
            df_historico=gerenciador.pagina_3_inicializa_top_10_marcas_historico(),
        ),
    ],
    className="pagina",
    id="pagina_3",
)


clientside_callback(
    processamento_pagina_3.callback_verificar_datas(),
    Output("pagina_3_modal_erro_titulo", "children"),
    Output("pagina_3_modal_erro_conteudo", "children"),
    Input("pagina_3_botao", "n_clicks"),
    State("pagina_3_seletor_datas", "start_date"),
    State("pagina_3_seletor_datas", "end_date"),
    State("pagina_3_periodo_hoje", "children"),
    State("pagina_3_periodo_escolhido", "children"),
    State("pagina_3_periodo_historico", "children"),
    prevent_initial_call=True,
)


clientside_callback(
    processamento_pagina_3.callback_abrir_modal(),
    Output("pagina_3_modal_erro", "is_open"),
    Input("pagina_3_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


@callback(
    Output("pagina_3_grafico_top_10_marcas_escolhido", "figure"),
    Output("pagina_3_seletor_datas", "start_date"),
    Output("pagina_3_seletor_datas", "end_date"),
    Output("pagina_3_periodo_escolhido", "children"),
    Input("pagina_3_modal_erro_titulo", "children"),
    State("pagina_3_seletor_datas", "start_date"),
    State("pagina_3_seletor_datas", "end_date"),
    prevent_initial_call=True,
)
def pagina_3_atualizar_comparacao(titulo, data_inicio, data_fim):
    if titulo != "":
        raise PreventUpdate

    df_novo = gerenciador.pagina_3_atualiza_top_10_marcas_periodo(
        data_inicio, data_fim
    )

    periodo_novo = processamento_pagina_3.retorna_periodo_novo(
        data_inicio=data_inicio, data_fim=data_fim
    )

    patch_figura = Patch()

    patch_figura["data"][0]["x"] = df_novo["Marca"].values
    patch_figura["data"][0]["y"] = df_novo["Porcentagem"].values

    return patch_figura, None, None, periodo_novo
