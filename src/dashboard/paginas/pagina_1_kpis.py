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


layout = html.Div(
    [
        # titulo(),
        div_seletor_datas_e_botao(),
        modal_erro(),
        Row(
            [
                Col(
                    gerenciador.pagina_1_inicializa_coluna_hoje(),
                    width=4,
                    class_name="coluna_atual",
                ),
                Col(
                    gerenciador.pagina_1_inicializa_coluna_escolhido(),
                    width=4,
                    class_name="coluna_escolhido",
                ),
                Col(
                    gerenciador.pagina_1_inicializa_coluna_historico(),
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

clientside_callback(
    processamento_pagina_1.callback_verificar_datas(),
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


@callback(
    Output("pagina_1_periodo_escolhido", "children"),
    Output("pagina_1_valor_num_produtos_escolhido", "children"),
    Output("pagina_1_valor_num_marcas_escolhido", "children"),
    Output("pagina_1_valor_media_precos_escolhido", "children"),
    Output("pagina_1_valor_num_produtos_promocoes_escolhido", "children"),
    Output("pagina_1_valor_num_marcas_promocoes_escolhido", "children"),
    Output("pagina_1_valor_percentual_medio_desconto_escolhido", "children"),
    Output("pagina_1_valor_produtos_abaixo_200_escolhido", "children"),
    Output("pagina_1_valor_num_produtos_nota_maior_4_escolhido", "children"),
    Output(
        "pagina_1_valor_num_produtos_20_ou_mais_avaliacoes_escolhido",
        "children",
    ),
    Output("pagina_1_valor_num_produtos_sem_avaliacoes_escolhido", "children"),
    Output("pagina_1_seletor_datas", "start_date"),
    Output("pagina_1_seletor_datas", "end_date"),
    Input("pagina_1_modal_erro_titulo", "children"),
    State("pagina_1_seletor_datas", "start_date"),
    State("pagina_1_seletor_datas", "end_date"),
    prevent_initial_call=True,
)
def pagina_2_atualizar_dados_periodo_escolhido(titulo, data_inicio, data_fim):
    if titulo != "":
        raise PreventUpdate

    return [
        *gerenciador.pagina_1_atualiza_coluna_escolhido(data_inicio, data_fim),
        None,
        None,
    ]


clientside_callback(
    processamento_pagina_1.callback_abrir_modal(),
    Output("pagina_1_modal_erro", "is_open"),
    Input("pagina_1_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


clientside_callback(
    processamento_pagina_1.callback_ranking_direto_valores(),
    Output("pagina_1_ranking_num_produtos_escolhido", "className"),
    Output("pagina_1_ranking_num_produtos_hoje", "className"),
    Output("pagina_1_ranking_num_produtos_historico", "className"),
    Input("pagina_1_valor_num_produtos_escolhido", "children"),
    State("pagina_1_valor_num_produtos_hoje", "children"),
    State("pagina_1_valor_num_produtos_historico", "children"),
)

clientside_callback(
    processamento_pagina_1.callback_ranking_direto_valores(),
    Output("pagina_1_ranking_num_marcas_escolhido", "className"),
    Output("pagina_1_ranking_num_marcas_hoje", "className"),
    Output("pagina_1_ranking_num_marcas_historico", "className"),
    Input("pagina_1_valor_num_marcas_escolhido", "children"),
    State("pagina_1_valor_num_marcas_hoje", "children"),
    State("pagina_1_valor_num_marcas_historico", "children"),
)


clientside_callback(
    processamento_pagina_1.callback_ranking_direto_valores(),
    Output("pagina_1_ranking_num_produtos_promocoes_escolhido", "className"),
    Output("pagina_1_ranking_num_produtos_promocoes_hoje", "className"),
    Output("pagina_1_ranking_num_produtos_promocoes_historico", "className"),
    Input("pagina_1_valor_num_produtos_promocoes_escolhido", "children"),
    State("pagina_1_valor_num_produtos_promocoes_hoje", "children"),
    State("pagina_1_valor_num_produtos_promocoes_historico", "children"),
)

clientside_callback(
    processamento_pagina_1.callback_ranking_direto_valores(),
    Output("pagina_1_ranking_num_marcas_promocoes_escolhido", "className"),
    Output("pagina_1_ranking_num_marcas_promocoes_hoje", "className"),
    Output("pagina_1_ranking_num_marcas_promocoes_historico", "className"),
    Input("pagina_1_valor_num_marcas_promocoes_escolhido", "children"),
    State("pagina_1_valor_num_marcas_promocoes_hoje", "children"),
    State("pagina_1_valor_num_marcas_promocoes_historico", "children"),
)


clientside_callback(
    processamento_pagina_1.callback_ranking_direto_valores(),
    Output("pagina_1_ranking_produtos_abaixo_200_escolhido", "className"),
    Output("pagina_1_ranking_produtos_abaixo_200_hoje", "className"),
    Output("pagina_1_ranking_produtos_abaixo_200_historico", "className"),
    Input("pagina_1_valor_produtos_abaixo_200_escolhido", "children"),
    State("pagina_1_valor_produtos_abaixo_200_hoje", "children"),
    State("pagina_1_valor_produtos_abaixo_200_historico", "children"),
)


clientside_callback(
    processamento_pagina_1.callback_ranking_direto_valores(),
    Output("pagina_1_ranking_percentual_medio_desconto_escolhido", "className"),
    Output("pagina_1_ranking_percentual_medio_desconto_hoje", "className"),
    Output("pagina_1_ranking_percentual_medio_desconto_historico", "className"),
    Input("pagina_1_valor_percentual_medio_desconto_escolhido", "children"),
    State("pagina_1_valor_percentual_medio_desconto_hoje", "children"),
    State("pagina_1_valor_percentual_medio_desconto_historico", "children"),
)


clientside_callback(
    processamento_pagina_1.callback_ranking_inverso_valores(),
    Output("pagina_1_ranking_media_precos_escolhido", "className"),
    Output("pagina_1_ranking_media_precos_hoje", "className"),
    Output("pagina_1_ranking_media_precos_historico", "className"),
    Input("pagina_1_valor_media_precos_escolhido", "children"),
    State("pagina_1_valor_media_precos_hoje", "children"),
    State("pagina_1_valor_media_precos_historico", "children"),
)


clientside_callback(
    processamento_pagina_1.callback_ranking_direto_valores(),
    Output(
        "pagina_1_ranking_num_produtos_20_ou_mais_avaliacoes_escolhido",
        "className",
    ),
    Output(
        "pagina_1_ranking_num_produtos_20_ou_mais_avaliacoes_hoje", "className"
    ),
    Output(
        "pagina_1_ranking_num_produtos_20_ou_mais_avaliacoes_historico",
        "className",
    ),
    Input(
        "pagina_1_valor_num_produtos_20_ou_mais_avaliacoes_escolhido",
        "children",
    ),
    State("pagina_1_valor_num_produtos_20_ou_mais_avaliacoes_hoje", "children"),
    State(
        "pagina_1_valor_num_produtos_20_ou_mais_avaliacoes_historico",
        "children",
    ),
)


clientside_callback(
    processamento_pagina_1.callback_ranking_inverso_valores(),
    Output(
        "pagina_1_ranking_num_produtos_sem_avaliacoes_escolhido", "className"
    ),
    Output("pagina_1_ranking_num_produtos_sem_avaliacoes_hoje", "className"),
    Output(
        "pagina_1_ranking_num_produtos_sem_avaliacoes_historico", "className"
    ),
    Input("pagina_1_valor_num_produtos_sem_avaliacoes_escolhido", "children"),
    State("pagina_1_valor_num_produtos_sem_avaliacoes_hoje", "children"),
    State("pagina_1_valor_num_produtos_sem_avaliacoes_historico", "children"),
)


clientside_callback(
    processamento_pagina_1.callback_ranking_direto_valores(),
    Output("pagina_1_ranking_num_produtos_nota_maior_4_escolhido", "className"),
    Output("pagina_1_ranking_num_produtos_nota_maior_4_hoje", "className"),
    Output("pagina_1_ranking_num_produtos_nota_maior_4_historico", "className"),
    Input("pagina_1_valor_num_produtos_nota_maior_4_escolhido", "children"),
    State("pagina_1_valor_num_produtos_nota_maior_4_hoje", "children"),
    State("pagina_1_valor_num_produtos_nota_maior_4_historico", "children"),
)
