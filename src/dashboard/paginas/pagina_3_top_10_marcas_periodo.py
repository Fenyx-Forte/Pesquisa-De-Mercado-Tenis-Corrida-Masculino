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
    Modal,
    ModalBody,
    ModalHeader,
    ModalTitle,
)
from pandas import DataFrame as pd_DataFrame

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


def botao_adicionar_grafico() -> Button:
    conteudo = Button(
        "Adicionar Gráfico",
        outline=True,
        color="primary",
        className="me-1",
        id="pagina_3_botao",
        class_name="botao",
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


def modal_sucesso() -> Modal:
    conteudo = Modal(
        [
            ModalHeader(
                ModalTitle(
                    "Gráfico Adicionado", id="pagina_3_modal_sucesso_titulo"
                )
            ),
            ModalBody(
                "Para ver o gráfico, role a tela para baixo.",
                id="pagina_3_modal_sucesso_conteudo",
            ),
        ],
        id="pagina_3_modal_sucesso",
        is_open=False,
    )

    return conteudo


def configuracoes_grafico():
    configuracoes = {
        "responsive": True,
        "config": {
            "displayModeBar": False,
            "doubleClick": False,
            "editSelection": False,
            "editable": False,
            "scrollZoom": False,
            "showTips": False,
        },
    }

    return configuracoes


def figura_top_10_marcas(df: pd_DataFrame, cor: str) -> px.bar:
    figura = (
        px.bar(
            df,
            x="Marca",
            y="Porcentagem",
            color="Periodo",
            labels={"Periodo": "Período"},
            color_discrete_sequence=[cor],
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
            uniformtext_mode="hide",
            legend=dict(
                font=dict(size=14, color="black"),
            ),
        )
    )

    return figura


layout = html.Div(
    [
        # titulo(),
        # html.Br(),
        seletor_datas(),
        botao_adicionar_grafico(),
        modal_erro(),
        modal_sucesso(),
        html.Div(
            dcc.Graph(
                figure=figura_top_10_marcas(
                    df=gerenciador.pagina_3_top_10_marcas_historico(),
                    cor="#6495ED",
                ),
                id="grafico-top-10-marcas-1",
                **configuracoes_grafico(),
            ),
            id="pagina_3_div_1",
        ),
        html.Div(
            dcc.Graph(
                id="grafico-top-10-marcas-2",
                **configuracoes_grafico(),
            ),
            id="pagina_3_div_2",
            style={"display": "none"},
        ),
        html.Div(
            dcc.Graph(
                id="grafico-top-10-marcas-3",
                **configuracoes_grafico(),
            ),
            id="pagina_3_div_3",
            style={"display": "none"},
        ),
    ],
    className="pagina",
    id="pagina_3",
)


@callback(
    Output("pagina_3_modal_erro_titulo", "children"),
    Output("pagina_3_modal_erro_conteudo", "children"),
    Input("pagina_3_botao", "n_clicks"),
    State("pagina_3_seletor_datas", "start_date"),
    State("pagina_3_seletor_datas", "end_date"),
    State("grafico-top-10-marcas-1", "figure"),
    State("grafico-top-10-marcas-2", "figure"),
    State("grafico-top-10-marcas-3", "figure"),
    prevent_initial_call=True,
)
def pagina_3_verificar_inputs(
    n_clicks, data_inicio, data_fim, grafico_1, grafico_2, grafico_3
):
    titulo = ""
    conteudo = ""

    if not processamento_pagina_3.verifica_se_datas_sao_validas(
        data_inicio, data_fim
    ):
        titulo = "Período Inválido"

        conteudo = "Selecione as datas usando o calendário ou escreva a data no formato DD/MM/YYYY."

        return titulo, conteudo

    if processamento_pagina_3.verifica_se_qtd_maxima_de_graficos_ja_foi_adicionada(
        grafico_2, grafico_3
    ):
        titulo = "Quantidade Máxima de Gráficos Atingida"

        conteudo = "A quantidade máxima de gráficos é 3."

        return titulo, conteudo

    if processamento_pagina_3.verifica_se_periodo_ja_foi_adicionado(
        data_inicio, data_fim, grafico_1, grafico_2
    ):
        titulo = "Período Já Adicionado"

        conteudo = (
            "Esse período já foi adicionado. Adicione um período diferente."
        )

        return titulo, conteudo

    # Nesse ponto, todas as validacoes ja foram feitas

    # O titulo do modal ira decidir o grafico que sera criado
    if grafico_2 is None:
        titulo = "2"

        return titulo, conteudo

    titulo = "3"

    return titulo, conteudo


clientside_callback(
    """
    function abrirModal(titulo) {
        if (titulo === "2" || titulo === "3") {
            return window.dash_clientside.no_update;
        }
        return true;
    }
    """,
    Output("pagina_3_modal_erro", "is_open"),
    Input("pagina_3_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


@callback(
    Output("grafico-top-10-marcas-2", "figure"),
    Output("pagina_3_div_2", "style"),
    Input("pagina_3_modal_erro_titulo", "children"),
    State("pagina_3_seletor_datas", "start_date"),
    State("pagina_3_seletor_datas", "end_date"),
    prevent_initial_call=True,
)
def pagina_3_adicionar_grafico_2(titulo, data_inicio, data_fim):
    if titulo != "2":
        raise PreventUpdate

    dados_grafico = gerenciador.pagina_3_top_10_marcas_periodo(
        data_inicio, data_fim
    )

    return figura_top_10_marcas(dados_grafico, "#FFA07A"), {"display": "inline"}


@callback(
    Output("grafico-top-10-marcas-3", "figure"),
    Output("pagina_3_div_3", "style"),
    Input("pagina_3_modal_erro_titulo", "children"),
    State("pagina_3_seletor_datas", "start_date"),
    State("pagina_3_seletor_datas", "end_date"),
    prevent_initial_call=True,
)
def pagina_3_adicionar_grafico_3(titulo, data_inicio, data_fim):
    if titulo != "3":
        raise PreventUpdate

    dados_grafico = gerenciador.pagina_3_top_10_marcas_periodo(
        data_inicio, data_fim
    )

    return figura_top_10_marcas(dados_grafico, "#5CB85C"), {"display": "inline"}


clientside_callback(
    """
    function limparSeletorDatas(n_clicks, style_2, style_3) {
        return [null, null];
    }
    """,
    Output("pagina_3_seletor_datas", "start_date"),
    Output("pagina_3_seletor_datas", "end_date"),
    Input("pagina_3_div_2", "style"),
    Input("pagina_3_div_3", "style"),
    prevent_initial_call=True,
)

clientside_callback(
    """
    function abrirModalSucesso(style_1, style_2) {
        return true;
    }
    """,
    Output("pagina_3_modal_sucesso", "is_open"),
    Input("pagina_3_div_2", "style"),
    Input("pagina_3_div_3", "style"),
    prevent_initial_call=True,
)
