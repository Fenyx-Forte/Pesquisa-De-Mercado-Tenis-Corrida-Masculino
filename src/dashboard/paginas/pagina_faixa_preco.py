"""Página Faixas Preço."""

from dash import (
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    html,
    register_page,
)
from dash.exceptions import PreventUpdate
from dash_ag_grid import AgGrid
from dash_bootstrap_components import (
    Col,
    Row,
)

from dashboard.processamento import gerenciador
from dashboard.uteis import (
    componentes_pagina,
    formatacoes,
    uteis_processamento,
)

register_page(
    __name__,
    path="/faixa-preco",
    name="Faixas Preço",
    title="Faixas Preço",
    description="Página Faixas de Preço",
    image_url="https://analise-de-dados-tenis-corrida.onrender.com/assets/images/imagem_link.jpg",
)


def id_pagina() -> str:
    """Id da página.

    Returns:
        str: id da página.
    """
    return "faixa_preco"


def titulo_pagina() -> str:
    """Título da página.

    Returns:
        str: Título da página.
    """
    return "Faixas de Preço"


def definicoes_colunas_tabela(sufixo_coluna: str) -> list[dict]:
    """Retorna uma lista de dicionários que representam as definições das colunas da tabela.

    Args:
        sufixo_coluna (str): Sufixo que define qual configuração será usada.

    Returns:
        list[dict]: Configuração a ser usada pela tabela a depender de sufixo_coluna.
    """
    configuracao_marca = {
        "headerName": "Marca",
        "field": "marca",
        "cellDataType": "text",
    }

    configuracao_num_produtos_hoje = {
        "headerName": "Produtos",
        "field": "num_produtos",
        "headerTooltip": "Quantidade de Produtos",
        "cellDataType": "number",
    }

    configuracao_num_produtos_periodo = {
        "headerName": "Produtos",
        "field": "num_produtos",
        "headerTooltip": "Quantidade de Produtos",
        "cellDataType": "number",
        "valueFormatter": {
            "function": f"{formatacoes.dag_format_pt_br()}.format('.2f')(params.value)",
        },
    }

    if sufixo_coluna == "hoje":
        return [
            configuracao_marca,
            configuracao_num_produtos_hoje,
        ]

    return [
        configuracao_marca,
        configuracao_num_produtos_periodo,
    ]


def informacao(tabela: AgGrid) -> html.Div:
    """Retorna uma Div contendo a tabela.

    Args:
        tabela (AgGrid): Tabela com as informações.

    Returns:
        html.Div: Div contendo a tabela.
    """
    return html.Div(
        html.Div(
            tabela,
            className="tabela",
        ),
        className="informacao",
    )


def coluna(
    titulo_cabecalho: str,
    periodo: str,
    sufixo_coluna: str,
    dados_abaixo_de_200: list[dict],
    dados_entre_200_e_400: list[dict],
    dados_acima_de_400: list[dict],
) -> html.Div:
    """Retorna uma das 3 colunas usadas no corpo da página.

    Args:
        titulo_cabecalho (str): Título do cabeçalho da coluna.
        periodo (str): Período utilizado para filtrar os dados.
        sufixo_coluna (str): Sufixo que será adicionado ao nome das colunas para criar as definições das colunas.
        dados_abaixo_de_200 (list[dict]): Dados com valor abaixo de 200.
        dados_entre_200_e_400 (list[dict]): Dados com valor entre 200 e 400.
        dados_acima_de_400 (list[dict]): Dados com valor acima de 400.

    Returns:
        html.Div: Coluna que será usada no corpo da página.
    """
    tabela_abaixo_de_200 = componentes_pagina.tabela_ag_grid(
        dados=dados_abaixo_de_200,
        id_completo=f"{id_pagina()}_tabela_{sufixo_coluna}_200",
        definicoes_colunas=definicoes_colunas_tabela(sufixo_coluna),
    )

    tabela_entre_200_e_400 = componentes_pagina.tabela_ag_grid(
        dados=dados_entre_200_e_400,
        id_completo=f"{id_pagina()}_tabela_{sufixo_coluna}_200_400",
        definicoes_colunas=definicoes_colunas_tabela(sufixo_coluna),
    )

    tabela_acima_de_400 = componentes_pagina.tabela_ag_grid(
        dados=dados_acima_de_400,
        id_completo=f"{id_pagina()}_tabela_{sufixo_coluna}_400",
        definicoes_colunas=definicoes_colunas_tabela(sufixo_coluna),
    )

    return html.Div(
        [
            componentes_pagina.cabecalho_coluna(
                id_pagina=id_pagina(),
                sufixo_coluna=sufixo_coluna,
                titulo=titulo_cabecalho,
                periodo=periodo,
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Preço Abaixo de R$200",
                informacao=informacao(tabela_abaixo_de_200),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Preço Entre R$200 e R$400",
                informacao=informacao(tabela_entre_200_e_400),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Preço Acima de R$400",
                informacao=informacao(tabela_acima_de_400),
            ),
        ],
    )


def colunas() -> Row:
    """Retorna um conjunto de colunas.

    Returns:
        Row: Linha que contém todas as colunas do corpo da página.
    """
    periodo_hoje = gerenciador.retorna_periodo_hoje()

    periodo_escolhido = gerenciador.retorna_periodo_ultima_semana()

    periodo_historico = gerenciador.retorna_periodo_historico()

    dados_hoje = gerenciador.pagina_faixa_preco_dados_hoje()

    dados_escolhido = gerenciador.pagina_faixa_preco_dados_ultima_semana()

    dados_historico = gerenciador.pagina_faixa_preco_dados_historico()

    return Row(
        [
            Col(
                coluna(
                    titulo_cabecalho="Hoje",
                    periodo=periodo_hoje,
                    sufixo_coluna="hoje",
                    **dados_hoje,
                ),
                xs=12,
                md=6,
                xl=4,
                class_name="coluna_hoje",
            ),
            Col(
                coluna(
                    titulo_cabecalho="Período Escolhido",
                    periodo=periodo_escolhido,
                    sufixo_coluna="escolhido",
                    **dados_escolhido,
                ),
                xs=12,
                md=6,
                xl=4,
                class_name="coluna_escolhido",
            ),
            Col(
                coluna(
                    titulo_cabecalho="Histórico",
                    periodo=periodo_historico,
                    sufixo_coluna="historico",
                    **dados_historico,
                ),
                xs=12,
                md=6,
                xl=4,
                class_name="coluna_historico",
            ),
        ],
        class_name="linha_colunas",
    )


layout = html.Div(
    [
        componentes_pagina.div_titulo(titulo_pagina()),
        componentes_pagina.div_seletor_datas_e_botao(
            id_pagina=id_pagina(),
            data_mais_antiga=gerenciador.retorna_data_coleta_mais_antiga(),
            data_mais_recente=gerenciador.retorna_data_coleta_mais_recente(),
        ),
        componentes_pagina.modal_erro(id_pagina()),
        colunas(),
    ],
    className="pagina",
    id=id_pagina(),
)


clientside_callback(
    uteis_processamento.callback_verificar_datas(),
    Output(f"{id_pagina()}_modal_erro_titulo", "children"),
    Output(f"{id_pagina()}_modal_erro_conteudo", "children"),
    Input(f"{id_pagina()}_botao", "n_clicks"),
    State(f"{id_pagina()}_seletor_datas", "start_date"),
    State(f"{id_pagina()}_seletor_datas", "end_date"),
    State(f"{id_pagina()}_periodo_hoje", "children"),
    State(f"{id_pagina()}_periodo_escolhido", "children"),
    State(f"{id_pagina()}_periodo_historico", "children"),
    prevent_initial_call=True,
)


clientside_callback(
    uteis_processamento.callback_abrir_modal(),
    Output(f"{id_pagina()}_modal_erro", "is_open"),
    Input(f"{id_pagina()}_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


@callback(
    Output(f"{id_pagina()}_tabela_escolhido_200", "rowData"),
    Output(f"{id_pagina()}_tabela_escolhido_200_400", "rowData"),
    Output(f"{id_pagina()}_tabela_escolhido_400", "rowData"),
    Output(f"{id_pagina()}_seletor_datas", "start_date"),
    Output(f"{id_pagina()}_seletor_datas", "end_date"),
    Output(f"{id_pagina()}_periodo_escolhido", "children"),
    Input(f"{id_pagina()}_modal_erro_titulo", "children"),
    State(f"{id_pagina()}_seletor_datas", "start_date"),
    State(f"{id_pagina()}_seletor_datas", "end_date"),
    prevent_initial_call=True,
    running=[(Output(f"{id_pagina()}_botao", "disabled"), True, False)],
)
def faixa_preco_atualiza_dados_periodo_escolhido(
    titulo: str,
    data_inicio: str,
    data_fim: str,
) -> list[dict | None | str]:
    """Retorna os dados atualizados da coluna "escolhido" para um período especificado.

    Args:
        titulo (str): Título atual do modal_erro. Se não for igual a "", então houve algum erro detectado pelo modal_erro.
        data_inicio (str): Data de início do período a ser considerado.
        data_fim (str): Data de fim do período a ser considerado.

    Returns:
        list[dict | None | str]: Lista com os dados necessários para atualizar a coluna.
    """
    if titulo != "":
        raise PreventUpdate

    if not gerenciador.valida_entrada_datas(data_inicio, data_fim):
        raise PreventUpdate

    periodo_novo = uteis_processamento.retorna_periodo(data_inicio, data_fim)

    dados_escolhido = gerenciador.pagina_faixa_preco_atualiza_dados_escolhido(
        data_inicio,
        data_fim,
    )

    return [
        dados_escolhido["dados_abaixo_de_200"],
        dados_escolhido["dados_entre_200_e_400"],
        dados_escolhido["dados_acima_de_400"],
        None,
        None,
        periodo_novo,
    ]


clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_hoje_200", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_hoje_200", "virtualRowData"),
    State(f"{id_pagina()}_tabela_hoje_200", "dashGridOptions"),
    prevent_initial_call=True,
)


clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_escolhido_200", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_escolhido_200", "virtualRowData"),
    State(f"{id_pagina()}_tabela_escolhido_200", "dashGridOptions"),
    prevent_initial_call=True,
)

clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_historico_200", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_historico_200", "virtualRowData"),
    State(f"{id_pagina()}_tabela_historico_200", "dashGridOptions"),
    prevent_initial_call=True,
)


clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_hoje_200_400", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_hoje_200_400", "virtualRowData"),
    State(f"{id_pagina()}_tabela_hoje_200_400", "dashGridOptions"),
    prevent_initial_call=True,
)


clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_escolhido_200_400", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_escolhido_200_400", "virtualRowData"),
    State(f"{id_pagina()}_tabela_escolhido_200_400", "dashGridOptions"),
    prevent_initial_call=True,
)

clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_historico_200_400", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_historico_200_400", "virtualRowData"),
    State(f"{id_pagina()}_tabela_historico_200_400", "dashGridOptions"),
    prevent_initial_call=True,
)


clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_hoje_400", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_hoje_400", "virtualRowData"),
    State(f"{id_pagina()}_tabela_hoje_400", "dashGridOptions"),
    prevent_initial_call=True,
)


clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_escolhido_400", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_escolhido_400", "virtualRowData"),
    State(f"{id_pagina()}_tabela_escolhido_400", "dashGridOptions"),
    prevent_initial_call=True,
)

clientside_callback(
    uteis_processamento.callback_linha_totais_faixa_preco(),
    Output(f"{id_pagina()}_tabela_historico_400", "dashGridOptions"),
    Input(f"{id_pagina()}_tabela_historico_400", "virtualRowData"),
    State(f"{id_pagina()}_tabela_historico_400", "dashGridOptions"),
    prevent_initial_call=True,
)
