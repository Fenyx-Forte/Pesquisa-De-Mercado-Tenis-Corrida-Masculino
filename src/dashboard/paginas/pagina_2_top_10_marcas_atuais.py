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


def botao_adicionar_periodo() -> Button:
    conteudo = Button(
        "Adicionar Período",
        outline=True,
        color="primary",
        className="me-1",
        id="pagina_2_botao",
        class_name="botao",
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
            labels={"Periodo": "Período"},
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
        id="pagina_2_grafico_top_10_marcas",
    )

    return conteudo


layout = html.Div(
    [
        # titulo(),
        # html.Br(),
        seletor_datas(),
        botao_adicionar_periodo(),
        modal_erro(),
        grafico_top_10_marcas(),
    ],
    className="pagina",
    id="pagina_2",
)


@callback(
    Output("pagina_2_modal_erro_titulo", "children"),
    Output("pagina_2_modal_erro_conteudo", "children"),
    Input("pagina_2_botao", "n_clicks"),
    State("pagina_2_seletor_datas", "start_date"),
    State("pagina_2_seletor_datas", "end_date"),
    State("pagina_2_grafico_top_10_marcas", "figure"),
    prevent_initial_call=True,
)
def pagina_2_verificar_inputs(
    n_clicks, data_inicio, data_fim, dados_grafico_atual
):
    titulo = ""
    conteudo = ""

    if not processamento_pagina_2.verifica_se_datas_sao_validas(
        data_inicio, data_fim
    ):
        titulo = "Período Inválido"

        conteudo = "Selecione as datas usando o calendário ou escreva a data no formato DD/MM/YYYY."

        return titulo, conteudo

    if processamento_pagina_2.verifica_se_qtd_maxima_de_periodos_ja_foi_adicionada(
        dados_grafico_atual
    ):
        titulo = "Quantidade Máxima de Comparações Atingida"

        conteudo = "A quantidade máxima de comparações é 3."

        return titulo, conteudo

    if processamento_pagina_2.verifica_se_periodo_ja_foi_adicionado(
        data_inicio, data_fim, dados_grafico_atual
    ):
        titulo = "Período já Adicionado"

        conteudo = (
            "Esse período já foi adicionado. Adicione um período diferente."
        )

        return titulo, conteudo

    return titulo, conteudo


clientside_callback(
    """
    function abrirModal(titulo) {
        if (titulo === "") {
            return window.dash_clientside.no_update;
        }
        return true;
    }
    """,
    Output("pagina_2_modal_erro", "is_open"),
    Input("pagina_2_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


@callback(
    Output("pagina_2_grafico_top_10_marcas", "figure"),
    Output("pagina_2_seletor_datas", "start_date"),
    Output("pagina_2_seletor_datas", "end_date"),
    Input("pagina_2_modal_erro_titulo", "children"),
    State("pagina_2_seletor_datas", "start_date"),
    State("pagina_2_seletor_datas", "end_date"),
    State("pagina_2_grafico_top_10_marcas", "figure"),
    prevent_initial_call=True,
)
def pagina_2_adicionar_comparacao(
    titulo, data_inicio, data_fim, dados_grafico_atual
):
    if titulo != "":
        raise PreventUpdate

    dados_grafico = gerenciador.pagina_2_grafico_comparacao_top_10(
        dados_grafico_atual, data_inicio, data_fim
    )

    figura_nova = figura_top_10_marcas(dados_grafico)

    return figura_nova, None, None
