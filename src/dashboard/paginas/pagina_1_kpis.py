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
    Card,
    CardBody,
    Col,
    Modal,
    ModalBody,
    ModalHeader,
    ModalTitle,
    Row,
)

from dashboard.processamento import gerenciador
from dashboard.processamento.paginas import processamento_pagina_1

register_page(
    __name__,
    path="/kpis",
    name="KPI's",
    title="KPI's",
    description="Página KPI's",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1(
        "KPI's Principais",
        className="titulo-pagina",
    )

    return conteudo


def seletor_datas() -> dcc.DatePickerRange:
    conteudo = dcc.DatePickerRange(
        id="pagina_1_seletor_datas",
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
        "Atualizar",
        outline=True,
        color="primary",
        className="me-1",
        id="pagina_1_botao",
        class_name="botao",
    )

    return conteudo


def modal_erro() -> Modal:
    conteudo = Modal(
        [
            ModalHeader(ModalTitle("Titulo", id="pagina_1_modal_erro_titulo")),
            ModalBody("Conteudo", id="pagina_1_modal_erro_conteudo"),
        ],
        id="pagina_1_modal_erro",
        is_open=False,
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


def informacoes_coluna() -> html.Div:
    conteudo = html.Div(
        [
            html.Div(
                [
                    Card(
                        CardBody(
                            [
                                html.Div("Qtd Produtos"),
                                html.Div("500"),
                                html.Div(
                                    html.I(className="fa-solid fa-trophy"),
                                    className="ranking_top_1",
                                ),
                            ]
                        )
                    ),
                ],
                className="div_card",
            ),
            html.Br(),
            html.Div(
                [
                    Card(
                        CardBody(
                            [
                                html.Div("Qtd Produtos"),
                                html.Div("500"),
                                html.Div(
                                    html.I(className="fa-solid fa-trophy"),
                                    className="ranking_top_2",
                                ),
                            ]
                        )
                    ),
                ],
                className="div_card",
            ),
            html.Br(),
            html.Div(
                [
                    Card(
                        CardBody(
                            [
                                html.Div("Qtd Produtos"),
                                html.Div("500"),
                                html.Div(
                                    html.I(className="fa-solid fa-trophy"),
                                    className="ranking_top_3",
                                ),
                            ]
                        )
                    ),
                ],
                className="div_card",
            ),
        ],
        className="informacoes_coluna",
    )

    return conteudo


def coluna(
    titulo: str,
    periodo: str,
    id_periodo: str,
) -> html.Div:
    conteudo = html.Div(
        [
            html.H4(titulo, className="titulo_coluna"),
            html.Br(),
            html.Div(periodo, className="periodo_coluna", id=id_periodo),
            html.Br(),
            informacoes_coluna(),
        ],
    )

    return conteudo


layout = html.Div(
    [
        # titulo(),
        div_seletor_datas_e_botao(),
        modal_erro(),
        Row(
            [
                Col(
                    coluna(
                        titulo="Hoje",
                        periodo="12/09/2024 - 12/09/2024",
                        id_periodo="pagina_1_periodo_hoje",
                    ),
                    width=4,
                    class_name="coluna_atual",
                ),
                Col(
                    coluna(
                        titulo="Período Escolhido",
                        periodo="05/09/2024 - 12/09/2024",
                        id_periodo="pagina_1_periodo_escolhido",
                    ),
                    width=4,
                    class_name="coluna_usuario",
                ),
                Col(
                    coluna(
                        titulo="Período Histórico",
                        periodo="09/08/2024 - 12/09/2024",
                        id_periodo="pagina_1_periodo_historico",
                    ),
                    width=4,
                    class_name="coluna_historico",
                ),
            ],
            class_name="linha_colunas_kpis",
        ),
    ],
    className="pagina",
    id="pagina_1",
)


@callback(
    Output("pagina_1_modal_erro_titulo", "children"),
    Output("pagina_1_modal_erro_conteudo", "children"),
    Input("pagina_1_botao", "n_clicks"),
    State("pagina_1_seletor_datas", "start_date"),
    State("pagina_1_seletor_datas", "end_date"),
    State("pagina_1_periodo_hoje", "children"),
    State("pagina_1_periodo_escolhido", "children"),
    State("pagina_1_periodo_historico", "children"),
    prevent_initial_call=True,
)
def pagina_2_verificar_inputs(
    n_clicks,
    data_inicio,
    data_fim,
    periodo_hoje,
    periodo_ja_escolhido,
    periodo_historico,
):
    titulo = ""
    conteudo = ""

    if not processamento_pagina_1.verifica_se_datas_sao_validas(
        data_inicio, data_fim
    ):
        titulo = "Período Inválido"

        conteudo = "Selecione as datas usando o calendário ou escreva as datas no formato DD/MM/YYYY."

        return titulo, conteudo

    if processamento_pagina_1.verifica_se_periodo_ja_foi_adicionado(
        data_inicio,
        data_fim,
        periodo_hoje,
        periodo_ja_escolhido,
        periodo_historico,
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
    Output("pagina_1_modal_erro", "is_open"),
    Input("pagina_1_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)
