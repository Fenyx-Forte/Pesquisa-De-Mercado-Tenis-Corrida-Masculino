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
from dashboard.processamento.paginas import processamento_pagina_7
from dashboard.uteis import formatacoes, traducoes

register_page(
    __name__,
    path="/promocoes",
    name="Promoções",
    title="Promoções",
    description="Página Promoções",
    image_url="/assets/images/imagem_link.jpg",
)


def seletor_datas() -> dcc.DatePickerRange:
    conteudo = dcc.DatePickerRange(
        id="pagina_7_seletor_datas",
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
        id="pagina_7_botao",
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
            ModalHeader(ModalTitle("Titulo", id="pagina_7_modal_erro_titulo")),
            ModalBody("Conteudo", id="pagina_7_modal_erro_conteudo"),
        ],
        id="pagina_7_modal_erro",
        is_open=False,
    )

    return conteudo


def configuracoes_colunas_tabela(sufixo_coluna: str) -> list[dict]:
    configuracao_marca = {
        "headerName": "Marca",
        "field": "marca",
        "cellDataType": "text",
    }

    configuracao_produtos_hoje = {
        "headerName": "Produtos",
        "field": "produtos",
        "headerTooltip": "Quantidade de produtos",
        "cellDataType": "number",
    }

    configuracao_produtos_periodo = {
        "headerName": "Produtos",
        "field": "produtos",
        "headerTooltip": "Quantidade de produtos",
        "cellDataType": "number",
        "valueFormatter": {
            "function": f"{formatacoes.dag_format_pt_br()}.format('.2f')(params.value)",
        },
    }

    configuracao_desconto = {
        "headerName": "Desconto Médio (%)",
        "field": "desconto",
        "cellDataType": "number",
        "valueFormatter": {
            "function": f"{formatacoes.dag_format_pt_br()}.format('.2f')(params.value)",
        },
    }

    if sufixo_coluna == "hoje":
        return [
            configuracao_marca,
            configuracao_produtos_hoje,
            configuracao_desconto,
        ]

    else:
        return [
            configuracao_marca,
            configuracao_produtos_periodo,
            configuracao_desconto,
        ]


def tabela(
    dados: list[dict],
    sufixo_coluna: str,
) -> AgGrid:
    conteudo = AgGrid(
        rowData=dados,
        id=f"pagina_7_tabela_{sufixo_coluna}",
        columnDefs=configuracoes_colunas_tabela(sufixo_coluna),
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
    dados: list[dict],
) -> html.Div:
    conteudo = html.Div(
        [
            html.H4(titulo, className="titulo_coluna"),
            html.Br(),
            html.Div(
                periodo,
                className="periodo_coluna",
                id=f"pagina_7_periodo_{sufixo_coluna}",
            ),
            html.Br(),
            div_informacao(
                subtitulo_coluna="Promoções",
                dados=dados,
                sufixo_coluna=sufixo_coluna,
            ),
        ],
    )

    return conteudo


def linha_colunas() -> Row:
    periodo_hoje = gerenciador.retorna_periodo_hoje()

    periodo_escolhido = gerenciador.retorna_periodo_ultima_semana()

    periodo_historico = gerenciador.retorna_periodo_historico()

    dados_hoje = gerenciador.pagina_7_inicializa_dados_hoje()

    dados_escolhido = gerenciador.pagina_7_inicializa_dados_escolhido()

    dados_historico = gerenciador.pagina_7_inicializa_dados_historico()

    conteudo = Row(
        [
            Col(
                coluna(
                    titulo="Hoje",
                    periodo=periodo_hoje,
                    sufixo_coluna="hoje",
                    dados=dados_hoje,
                ),
                width=4,
                class_name="coluna_hoje",
            ),
            Col(
                coluna(
                    titulo="Período Escolhido",
                    periodo=periodo_escolhido,
                    sufixo_coluna="escolhido",
                    dados=dados_escolhido,
                ),
                width=4,
                class_name="coluna_escolhido",
            ),
            Col(
                coluna(
                    titulo="Histórico",
                    periodo=periodo_historico,
                    sufixo_coluna="historico",
                    dados=dados_historico,
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
    id="pagina_7",
)


clientside_callback(
    processamento_pagina_7.callback_verificar_datas(),
    Output("pagina_7_modal_erro_titulo", "children"),
    Output("pagina_7_modal_erro_conteudo", "children"),
    Input("pagina_7_botao", "n_clicks"),
    State("pagina_7_seletor_datas", "start_date"),
    State("pagina_7_seletor_datas", "end_date"),
    State("pagina_7_periodo_hoje", "children"),
    State("pagina_7_periodo_escolhido", "children"),
    State("pagina_7_periodo_historico", "children"),
    prevent_initial_call=True,
)


clientside_callback(
    processamento_pagina_7.callback_abrir_modal(),
    Output("pagina_7_modal_erro", "is_open"),
    Input("pagina_7_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


@callback(
    Output("pagina_7_tabela_escolhido", "rowData"),
    Output("pagina_7_seletor_datas", "start_date"),
    Output("pagina_7_seletor_datas", "end_date"),
    Output("pagina_7_periodo_escolhido", "children"),
    Input("pagina_7_modal_erro_titulo", "children"),
    State("pagina_7_seletor_datas", "start_date"),
    State("pagina_7_seletor_datas", "end_date"),
    prevent_initial_call=True,
)
def pagina_7_atualiza_dados_periodo_escolhido(titulo, data_inicio, data_fim):
    if titulo != "":
        raise PreventUpdate

    periodo_novo = processamento_pagina_7.retorna_periodo_novo(
        data_inicio, data_fim
    )

    dados = gerenciador.pagina_7_atualiza_dados_escolhido(data_inicio, data_fim)

    return (
        dados,
        None,
        None,
        periodo_novo,
    )
