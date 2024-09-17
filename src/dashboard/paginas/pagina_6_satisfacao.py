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
from dash_ag_grid import AgGrid
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
from dashboard.processamento.paginas import processamento_pagina_6
from dashboard.uteis import formatacoes, traducoes

register_page(
    __name__,
    path="/satisfacao",
    name="Satisfação",
    title="Satisfação",
    description="Página Satisfação",
    image_url="/assets/images/imagem_link.jpg",
)


def seletor_datas() -> dcc.DatePickerRange:
    conteudo = dcc.DatePickerRange(
        id="pagina_6_seletor_datas",
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
        id="pagina_6_botao",
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
            ModalHeader(ModalTitle("Titulo", id="pagina_6_modal_erro_titulo")),
            ModalBody("Conteudo", id="pagina_6_modal_erro_conteudo"),
        ],
        id="pagina_6_modal_erro",
        is_open=False,
    )

    return conteudo


def configuracoes_colunas_tabela(sufixo_informacao: str) -> list[dict]:
    configuracao_marca = {
        "headerName": "Marca",
        "field": "marca",
        "cellDataType": "text",
    }

    configuracao_nota = {
        "headerName": "Nota",
        "field": "nota_avaliacao",
        "headerTooltip": "Nota da Avaliação",
        "cellDataType": "number",
        "valueFormatter": {
            "function": f"{formatacoes.dag_format_pt_br()}.format('.2f')(params.value)",
        },
    }

    configuracao_num_avaliacoes = {
        "headerName": "Avaliações",
        "field": "num_avaliacoes",
        "headerTooltip": "Número de Avaliações",
        "cellDataType": "number",
        "valueFormatter": {
            "function": f"{formatacoes.dag_format_pt_br()}.format(',.2f')(params.value)",
        },
    }

    if sufixo_informacao == "nota_avaliacao":
        return [
            configuracao_marca,
            configuracao_nota,
            configuracao_num_avaliacoes,
        ]

    else:
        return [
            configuracao_marca,
            configuracao_num_avaliacoes,
            configuracao_nota,
        ]


def tabela(
    dados: list[dict], sufixo_coluna: str, sufixo_informacao: str
) -> AgGrid:
    conteudo = AgGrid(
        rowData=dados,
        id=f"pagina_6_tabela_{sufixo_coluna}_{sufixo_informacao}",
        columnDefs=configuracoes_colunas_tabela(sufixo_informacao),
        defaultColDef={
            "resizable": False,
            "filter": True,
            "headerClass": "center-aligned-header",
            "cellClass": "center-aligned-cell",
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
        },
        dashGridOptions={
            "animateRows": False,
            "suppressColumnMoveAnimation": True,
            "pagination": False,
            "tooltipShowDelay": 500,
            "alwaysMultiSort": True,
            "localeText": traducoes.dag_locale_pt_br(),
        },
        columnSize="responsiveSizeToFit",
        className="ag-theme-quartz tabela-dag",
    )

    return conteudo


def div_informacao(
    subtitulo_coluna: str,
    dados: list[dict],
    sufixo_coluna: str,
    sufixo_informacao: str,
) -> html.Div:
    conteudo = html.Div(
        [
            html.Div(
                subtitulo_coluna,
                className="subtitulo_coluna",
            ),
            html.Div(
                tabela(
                    dados=dados,
                    sufixo_coluna=sufixo_coluna,
                    sufixo_informacao=sufixo_informacao,
                ),
                className="div_tabela",
            ),
        ],
        className="div_informacao",
    )

    return conteudo


def coluna(
    titulo: str,
    periodo: str,
    sufixo_coluna: str,
    dados_mais_20_avaliacoes: list[dict],
    dados_nota_superior_4: list[dict],
) -> html.Div:
    conteudo = html.Div(
        [
            html.H4(titulo, className="titulo_coluna"),
            html.Br(),
            html.Div(
                periodo,
                className="periodo_coluna",
                id=f"pagina_6_periodo_{sufixo_coluna}",
            ),
            html.Br(),
            div_informacao(
                subtitulo_coluna="Marcas Com Mais de 20 Avaliações",
                dados=dados_mais_20_avaliacoes,
                sufixo_coluna=sufixo_coluna,
                sufixo_informacao="num_avaliacoes",
            ),
            div_informacao(
                subtitulo_coluna="Marcas Com Avaliações Superiores a 4",
                dados=dados_nota_superior_4,
                sufixo_coluna=sufixo_coluna,
                sufixo_informacao="nota_avaliacao",
            ),
        ],
    )

    return conteudo


def linha_colunas() -> Row:
    periodo_hoje = gerenciador.retorna_periodo_hoje()

    periodo_escolhido = gerenciador.retorna_periodo_ultima_semana()

    periodo_historico = gerenciador.retorna_periodo_historico()

    lista_dados_hoje = gerenciador.pagina_6_inicializa_dados_hoje()

    lista_dados_escolhido = gerenciador.pagina_6_inicializa_dados_escolhido()

    lista_dados_historico = gerenciador.pagina_6_inicializa_dados_historico()

    conteudo = Row(
        [
            Col(
                coluna(
                    titulo="Hoje",
                    periodo=periodo_hoje,
                    sufixo_coluna="hoje",
                    dados_mais_20_avaliacoes=lista_dados_hoje[0],
                    dados_nota_superior_4=lista_dados_hoje[1],
                ),
                width=4,
                class_name="coluna_hoje",
            ),
            Col(
                coluna(
                    titulo="Período Escolhido",
                    periodo=periodo_escolhido,
                    sufixo_coluna="escolhido",
                    dados_mais_20_avaliacoes=lista_dados_escolhido[0],
                    dados_nota_superior_4=lista_dados_escolhido[1],
                ),
                width=4,
                class_name="coluna_escolhido",
            ),
            Col(
                coluna(
                    titulo="Histórico",
                    periodo=periodo_historico,
                    sufixo_coluna="historico",
                    dados_mais_20_avaliacoes=lista_dados_historico[0],
                    dados_nota_superior_4=lista_dados_historico[1],
                ),
                width=4,
                class_name="coluna_historico",
            ),
        ],
        class_name="linha_colunas",
    )

    return conteudo


layout = html.Div(
    [
        div_seletor_datas_e_botao(),
        modal_erro(),
        linha_colunas(),
    ],
    className="pagina",
    id="pagina_6",
)


clientside_callback(
    processamento_pagina_6.callback_verificar_datas(),
    Output("pagina_6_modal_erro_titulo", "children"),
    Output("pagina_6_modal_erro_conteudo", "children"),
    Input("pagina_6_botao", "n_clicks"),
    State("pagina_6_seletor_datas", "start_date"),
    State("pagina_6_seletor_datas", "end_date"),
    State("pagina_6_periodo_hoje", "children"),
    State("pagina_6_periodo_escolhido", "children"),
    State("pagina_6_periodo_historico", "children"),
    prevent_initial_call=True,
)


clientside_callback(
    processamento_pagina_6.callback_abrir_modal(),
    Output("pagina_6_modal_erro", "is_open"),
    Input("pagina_6_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


@callback(
    Output("pagina_6_tabela_escolhido_num_avaliacoes", "rowData"),
    Output("pagina_6_tabela_escolhido_nota_avaliacao", "rowData"),
    Output("pagina_6_seletor_datas", "start_date"),
    Output("pagina_6_seletor_datas", "end_date"),
    Output("pagina_6_periodo_escolhido", "children"),
    Input("pagina_6_modal_erro_titulo", "children"),
    State("pagina_6_seletor_datas", "start_date"),
    State("pagina_6_seletor_datas", "end_date"),
    prevent_initial_call=True,
)
def pagina_6_atualiza_dados_periodo_escolhido(titulo, data_inicio, data_fim):
    if titulo != "":
        raise PreventUpdate

    periodo_novo = processamento_pagina_6.retorna_periodo_novo(
        data_inicio, data_fim
    )

    lista_dados = gerenciador.pagina_6_atualiza_dados_escolhido(
        data_inicio, data_fim
    )

    return (
        lista_dados[0],
        lista_dados[1],
        None,
        None,
        periodo_novo,
    )
