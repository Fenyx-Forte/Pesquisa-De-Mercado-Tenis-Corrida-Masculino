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


def cartao(
    titulo: str, valor: str, id_valor: str, ranking: str, id_ranking: str
) -> Card:
    conteudo = Card(
        CardBody(
            [
                html.Div(
                    titulo,
                    className="titulo_cartao",
                ),
                html.Div(
                    valor,
                    className="valor_cartao",
                    id=id_valor,
                ),
                html.Div(
                    html.I(className="fa-solid fa-trophy"),
                    className=ranking,
                    id=id_ranking,
                ),
            ]
        )
    )

    return conteudo


def div_cartao(
    titulo: str, valor: str, id_valor: str, ranking: str, id_ranking: str
) -> html.Div:
    conteudo = html.Div(
        cartao(
            titulo,
            valor,
            id_valor,
            ranking,
            id_ranking,
        ),
        className="div_card",
    )

    return conteudo


def informacoes_coluna() -> html.Div:
    conteudo = html.Div(
        [
            div_cartao("Qtd Produtos", "500", "ranking_top_1"),
            html.Br(),
            div_cartao("Qtd Produtos", "500", "ranking_top_2"),
            html.Br(),
            div_cartao("Qtd Produtos", "500", "ranking_top_3"),
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


clientside_callback(
    """
    function ranking_num_produtos(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
    Output("pagina_1_ranking_num_produtos_escolhido", "className"),
    Output("pagina_1_ranking_num_produtos_hoje", "className"),
    Output("pagina_1_ranking_num_produtos_historico", "className"),
    Input("pagina_1_valor_num_produtos_escolhido", "children"),
    State("pagina_1_valor_num_produtos_hoje", "children"),
    State("pagina_1_valor_num_produtos_historico", "children"),
)

clientside_callback(
    """
    function ranking_num_marcas(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
    Output("pagina_1_ranking_num_marcas_escolhido", "className"),
    Output("pagina_1_ranking_num_marcas_hoje", "className"),
    Output("pagina_1_ranking_num_marcas_historico", "className"),
    Input("pagina_1_valor_num_marcas_escolhido", "children"),
    State("pagina_1_valor_num_marcas_hoje", "children"),
    State("pagina_1_valor_num_marcas_historico", "children"),
)


clientside_callback(
    """
    function ranking_num_promocoes(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
    Output("pagina_1_ranking_num_promocoes_escolhido", "className"),
    Output("pagina_1_ranking_num_promocoes_hoje", "className"),
    Output("pagina_1_ranking_num_promocoes_historico", "className"),
    Input("pagina_1_valor_num_promocoes_escolhido", "children"),
    State("pagina_1_valor_num_promocoes_hoje", "children"),
    State("pagina_1_valor_num_promocoes_historico", "children"),
)


clientside_callback(
    """
    function ranking_produtos_abaixo_200(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
    Output("pagina_1_ranking_produtos_abaixo_200_escolhido", "className"),
    Output("pagina_1_ranking_produtos_abaixo_200_hoje", "className"),
    Output("pagina_1_ranking_produtos_abaixo_200_historico", "className"),
    Input("pagina_1_valor_produtos_abaixo_200_escolhido", "children"),
    State("pagina_1_valor_produtos_abaixo_200_hoje", "children"),
    State("pagina_1_valor_produtos_abaixo_200_historico", "children"),
)


clientside_callback(
    """
    function ranking_percentual_medio_desconto(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
    Output("pagina_1_ranking_percentual_medio_desconto_escolhido", "className"),
    Output("pagina_1_ranking_percentual_medio_desconto_hoje", "className"),
    Output("pagina_1_ranking_percentual_medio_desconto_historico", "className"),
    Input("pagina_1_valor_percentual_medio_desconto_escolhido", "children"),
    State("pagina_1_valor_percentual_medio_desconto_hoje", "children"),
    State("pagina_1_valor_percentual_medio_desconto_historico", "children"),
)


clientside_callback(
    """
    function ranking_media_precos(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
    Output("pagina_1_ranking_media_precos_escolhido", "className"),
    Output("pagina_1_ranking_media_precos_hoje", "className"),
    Output("pagina_1_ranking_media_precos_historico", "className"),
    Input("pagina_1_valor_media_precos_escolhido", "children"),
    State("pagina_1_valor_media_precos_hoje", "children"),
    State("pagina_1_valor_media_precos_historico", "children"),
)


clientside_callback(
    """
    function ranking_num_produtos_mais_20_avaliacoes(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
    Output(
        "pagina_1_ranking_num_produtos_mais_20_avaliacoes_escolhido",
        "className",
    ),
    Output(
        "pagina_1_ranking_num_produtos_mais_20_avaliacoes_hoje", "className"
    ),
    Output(
        "pagina_1_ranking_num_produtos_mais_20_avaliacoes_historico",
        "className",
    ),
    Input(
        "pagina_1_valor_num_produtos_mais_20_avaliacoes_escolhido", "children"
    ),
    State("pagina_1_valor_num_produtos_mais_20_avaliacoes_hoje", "children"),
    State(
        "pagina_1_valor_num_produtos_mais_20_avaliacoes_historico", "children"
    ),
)


clientside_callback(
    """
    function ranking_num_produtos_sem_avaliacoes(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
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
    """
    function ranking_num_produtos_nota_maior_4(str1, str2, str3) {
        // Converter strings para números
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        // Ordenar os números em ordem decrescente e remover duplicatas
        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        // Mapear cada número ao seu dense rank no formato "ranking_top_X"
        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """,
    Output("pagina_1_ranking_num_produtos_nota_maior_4_escolhido", "className"),
    Output("pagina_1_ranking_num_produtos_nota_maior_4_hoje", "className"),
    Output("pagina_1_ranking_num_produtos_nota_maior_4_historico", "className"),
    Input("pagina_1_valor_num_produtos_nota_maior_4_escolhido", "children"),
    State("pagina_1_valor_num_produtos_nota_maior_4_hoje", "children"),
    State("pagina_1_valor_num_produtos_nota_maior_4_historico", "children"),
)
