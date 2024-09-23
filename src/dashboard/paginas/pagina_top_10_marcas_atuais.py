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
from dash_bootstrap_components import (
    Col,
    Row,
)

from dashboard.processamento import gerenciador
from dashboard.uteis import componentes_pagina, uteis_processamento

register_page(
    __name__,
    path="/top-10-marcas-atuais",
    name="Top 10 Marcas Atuais",
    title="Top 10 Marcas Atuais",
    description="Top 10 Marcas Atuais",
    image_url="https://analise-de-dados-mercadolivre.onrender.com/assets/images/imagem_link.jpg",
)


def id_pagina() -> str:
    return "top_10_marcas_atuais"


def titulo_pagina() -> str:
    return "Top 10 Marcas Atuais"


def cabecalho_coluna(
    sufixo_coluna: str,
    titulo: str,
    periodo: str,
) -> html.Div:
    conteudo = html.Div(
        [
            html.H4(
                titulo,
                className="titulo_coluna",
            ),
            html.Br(),
            html.H5(
                periodo,
                className="periodo_coluna",
                id=f"{id_pagina()}_periodo_{sufixo_coluna}",
            ),
            html.Br(),
            html.Div(
                html.I(className="fa-solid fa-square"),
                className=f"legenda_{sufixo_coluna}",
            ),
        ],
        className="cabecalho_coluna",
    )

    return conteudo


def configuracoes_figura() -> dict:
    coluna_x = "Marca"

    coluna_y = "Porcentagem"

    coluna_divisao = "Periodo"

    cores = ["#6495ED", "#FFA07A", "#5CB85C"]

    labels = {
        "Periodo": "Período",
        "Porcentagem": "Porcentagem (%)",
    }

    hover_data = {
        "Porcentagem": ":.2f",
        "Periodo": False,
        "Marca": False,
    }

    return {
        "coluna_x": coluna_x,
        "coluna_y": coluna_y,
        "coluna_divisao": coluna_divisao,
        "cores": cores,
        "labels": labels,
        "hover_data": hover_data,
    }


def div_grafico_top_10_marcas() -> html.Div:
    df_grafico = gerenciador.pagina_top_10_marcas_atuais_dados_grafico()

    grafico = componentes_pagina.grafico_de_barras_agrupadas(
        df=df_grafico,
        id_grafico=f"{id_pagina()}_grafico",
        **configuracoes_figura(),
    )

    conteudo = html.Div(
        grafico,
        className="grafico",
    )

    return conteudo


def coluna(
    titulo_cabecalho: str,
    periodo: str,
    sufixo_coluna: str,
) -> html.Div:
    conteudo = html.Div(
        cabecalho_coluna(
            titulo=titulo_cabecalho,
            sufixo_coluna=sufixo_coluna,
            periodo=periodo,
        )
    )

    return conteudo


def colunas() -> Row:
    periodo_hoje = gerenciador.retorna_periodo_hoje()

    periodo_escolhido = gerenciador.retorna_periodo_ultima_semana()

    periodo_historico = gerenciador.retorna_periodo_historico()

    conteudo = Row(
        [
            Col(
                coluna(
                    titulo_cabecalho="Hoje",
                    sufixo_coluna="hoje",
                    periodo=periodo_hoje,
                ),
                width=4,
                class_name="coluna_hoje",
            ),
            Col(
                coluna(
                    titulo_cabecalho="Período Escolhido",
                    sufixo_coluna="escolhido",
                    periodo=periodo_escolhido,
                ),
                width=4,
                class_name="coluna_escolhido",
            ),
            Col(
                coluna(
                    titulo_cabecalho="Histórico",
                    sufixo_coluna="historico",
                    periodo=periodo_historico,
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
        componentes_pagina.div_titulo(titulo_pagina()),
        componentes_pagina.div_seletor_datas_e_botao(
            id_pagina=id_pagina(),
            data_mais_antiga=gerenciador.retorna_data_coleta_mais_antiga(),
            data_mais_recente=gerenciador.retorna_data_coleta_mais_recente(),
        ),
        componentes_pagina.modal_erro(id_pagina()),
        colunas(),
        div_grafico_top_10_marcas(),
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
    Output(f"{id_pagina()}_grafico", "figure"),
    Output(f"{id_pagina()}_seletor_datas", "start_date"),
    Output(f"{id_pagina()}_seletor_datas", "end_date"),
    Output(f"{id_pagina()}_periodo_escolhido", "children"),
    Input(f"{id_pagina()}_modal_erro_titulo", "children"),
    State(f"{id_pagina()}_seletor_datas", "start_date"),
    State(f"{id_pagina()}_seletor_datas", "end_date"),
    State(f"{id_pagina()}_grafico", "figure"),
    prevent_initial_call=True,
)
def top_10_marcas_atuais_atualizar_comparacao(
    titulo, data_inicio, data_fim, dados_grafico_atual
):
    if titulo != "":
        raise PreventUpdate

    df_atualizado = (
        gerenciador.pagina_top_10_marcas_atuais_atualizar_dados_grafico(
            dados_grafico_atual=dados_grafico_atual,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
    )

    figura_nova = componentes_pagina.figura_grafico_de_barras_agrupadas(
        df=df_atualizado, **configuracoes_figura()
    )

    periodo_novo = uteis_processamento.retorna_periodo(
        data_inicio=data_inicio, data_fim=data_fim
    )

    return figura_nova, None, None, periodo_novo
