import plotly.express as px
from dash import (
    Input,
    Output,
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
from dashboard.processamento.paginas import processamento_pagina_2

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
        id="pagina_2_seletor_datas",
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
        id="pagina_2_botao",
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
            ModalHeader(ModalTitle("Titulo", id="pagina_2_modal_erro_titulo")),
            ModalBody("Conteudo", id="pagina_2_modal_erro_conteudo"),
        ],
        id="pagina_2_modal_erro",
        is_open=False,
    )

    return conteudo


def figura_top_10_marcas(df: pd_DataFrame) -> Figure:
    figura = (
        px.bar(
            df,
            x="Marca",
            y="Porcentagem",
            color="Periodo",
            labels={
                "Periodo": "Período",
                "Porcentagem": "Porcentagem (%)",
            },
            color_discrete_sequence=["#6495ED", "#FFA07A", "#5CB85C"],
            barmode="group",
            hover_data={
                "Porcentagem": ":.2f",
                "Periodo": False,
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


def grafico_top_10_marcas() -> dcc.Graph:
    figura = figura_top_10_marcas(
        df=gerenciador.pagina_2_top_10_marcas_atuais()
    )

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
        id="pagina_2_grafico_top_10_marcas",
    )

    return conteudo


def div_periodo(titulo: str, periodo: str, sufixo: str) -> html.Div:
    conteudo = html.Div(
        [
            html.H4(titulo, className="titulo_coluna"),
            html.Br(),
            html.Div(
                periodo,
                className="periodo_coluna",
                id=f"pagina_2_periodo_{sufixo}",
            ),
            html.Br(),
            html.Div(
                html.I(className="fa-solid fa-square"),
                className=f"legenda_{sufixo}",
            ),
        ]
    )

    return conteudo


def colunas(
    periodo_hoje: str, periodo_escolhido: str, periodo_historico: str
) -> Row:
    conteudo = Row(
        [
            Col(
                div_periodo("Hoje", periodo_hoje, "hoje"),
                width=4,
                class_name="coluna_hoje",
            ),
            Col(
                div_periodo(
                    "Período Escolhido", periodo_escolhido, "escolhido"
                ),
                width=4,
                class_name="coluna_escolhido",
            ),
            Col(
                div_periodo("Histórico", periodo_historico, "historico"),
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
        div_seletor_datas_e_botao(),
        modal_erro(),
        colunas(
            periodo_hoje=gerenciador.retorna_periodo_hoje(),
            periodo_escolhido=gerenciador.retorna_periodo_ultima_semana(),
            periodo_historico=gerenciador.retorna_periodo_historico(),
        ),
        grafico_top_10_marcas(),
    ],
    className="pagina",
    id="pagina_2",
)


clientside_callback(
    processamento_pagina_2.callback_verificar_datas(),
    Output("pagina_2_modal_erro_titulo", "children"),
    Output("pagina_2_modal_erro_conteudo", "children"),
    Input("pagina_2_botao", "n_clicks"),
    State("pagina_2_seletor_datas", "start_date"),
    State("pagina_2_seletor_datas", "end_date"),
    State("pagina_2_periodo_hoje", "children"),
    State("pagina_2_periodo_escolhido", "children"),
    State("pagina_2_periodo_historico", "children"),
    prevent_initial_call=True,
)


clientside_callback(
    processamento_pagina_2.callback_abrir_modal(),
    Output("pagina_2_modal_erro", "is_open"),
    Input("pagina_2_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


@callback(
    Output("pagina_2_grafico_top_10_marcas", "figure"),
    Output("pagina_2_seletor_datas", "start_date"),
    Output("pagina_2_seletor_datas", "end_date"),
    Output("pagina_2_periodo_escolhido", "children"),
    Input("pagina_2_modal_erro_titulo", "children"),
    State("pagina_2_seletor_datas", "start_date"),
    State("pagina_2_seletor_datas", "end_date"),
    State("pagina_2_grafico_top_10_marcas", "figure"),
    prevent_initial_call=True,
)
def pagina_2_atualizar_comparacao(
    titulo, data_inicio, data_fim, dados_grafico_atual
):
    if titulo != "":
        raise PreventUpdate

    dados_grafico_atualizado = gerenciador.pagina_2_dados_grafico_atualizado(
        dados_grafico_atual=dados_grafico_atual,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

    figura_nova = figura_top_10_marcas(dados_grafico_atualizado)

    periodo_novo = processamento_pagina_2.retorna_periodo_novo(
        data_inicio=data_inicio, data_fim=data_fim
    )

    return figura_nova, None, None, periodo_novo
