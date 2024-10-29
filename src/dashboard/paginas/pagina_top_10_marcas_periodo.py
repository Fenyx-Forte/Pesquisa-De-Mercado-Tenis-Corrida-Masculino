from dash import (
    Input,
    Output,
    Patch,
    State,
    callback,
    clientside_callback,
    dcc,
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
    path="/top-10-marcas-periodo",
    name="Top 10 Marcas Período",
    title="Top 10 Marcas Período",
    description="Top 10 Marcas Período",
    image_url="https://analise-de-dados-mercadolivre.onrender.com/assets/images/imagem_link.jpg",
)


def id_pagina() -> str:
    return "top_10_marcas_periodo"


def titulo_pagina() -> str:
    return "Top 10 Marcas Período"


def configuracoes_figura(
    cor: str,
) -> dict:
    coluna_x = "Marca"

    coluna_y = "Porcentagem"

    labels = {
        "Porcentagem": "Porcentagem (%)",
    }

    hover_data = {
        "Porcentagem": ":.2f",
        "Marca": False,
    }

    return {
        "coluna_x": coluna_x,
        "coluna_y": coluna_y,
        "cor": cor,
        "labels": labels,
        "hover_data": hover_data,
    }


def informacao(grafico: dcc.Graph) -> html.Div:
    conteudo = html.Div(
        html.Div(
            grafico,
            className="grafico",
        ),
        className="informacao",
    )

    return conteudo


def coluna(
    sufixo_coluna: str,
    titulo_cabecalho: str,
    periodo: str,
    grafico: dcc.Graph,
) -> html.Div:
    conteudo = html.Div(
        [
            componentes_pagina.cabecalho_coluna(
                id_pagina=id_pagina(),
                sufixo_coluna=sufixo_coluna,
                titulo=titulo_cabecalho,
                periodo=periodo,
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Top 10 Marcas Período",
                informacao=informacao(grafico),
            ),
        ],
    )

    return conteudo


def colunas() -> Row:
    periodo_hoje = gerenciador.retorna_periodo_hoje()

    periodo_escolhido = gerenciador.retorna_periodo_ultima_semana()

    periodo_historico = gerenciador.retorna_periodo_historico()

    df_hoje = gerenciador.pagina_top_10_marcas_periodo_dados_hoje()

    df_escolhido = (
        gerenciador.pagina_top_10_marcas_periodo_dados_ultima_semana()
    )

    df_historico = gerenciador.pagina_top_10_marcas_periodo_dados_historico()

    grafico_hoje = componentes_pagina.grafico_de_barras_simples(
        df=df_hoje,
        id_grafico=f"{id_pagina()}_grafico_hoje",
        **configuracoes_figura("#6495ED"),
    )

    grafico_escolhido = componentes_pagina.grafico_de_barras_simples(
        df=df_escolhido,
        id_grafico=f"{id_pagina()}_grafico_escolhido",
        **configuracoes_figura("#FFA07A"),
    )

    grafico_historico = componentes_pagina.grafico_de_barras_simples(
        df=df_historico,
        id_grafico=f"{id_pagina()}_grafico_historico",
        **configuracoes_figura("#5CB85C"),
    )

    conteudo = Row(
        [
            Col(
                coluna(
                    sufixo_coluna="hoje",
                    titulo_cabecalho="Hoje",
                    periodo=periodo_hoje,
                    grafico=grafico_hoje,
                ),
                xs=12,
                md=6,
                xl=4,
                class_name="coluna_hoje",
            ),
            Col(
                coluna(
                    sufixo_coluna="escolhido",
                    titulo_cabecalho="Período Escolhido",
                    periodo=periodo_escolhido,
                    grafico=grafico_escolhido,
                ),
                xs=12,
                md=6,
                xl=4,
                class_name="coluna_escolhido",
            ),
            Col(
                coluna(
                    sufixo_coluna="historico",
                    titulo_cabecalho="Histórico",
                    periodo=periodo_historico,
                    grafico=grafico_historico,
                ),
                xs=12,
                md=6,
                xl=4,
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
    Output(f"{id_pagina()}_grafico_escolhido", "figure"),
    Output(f"{id_pagina()}_seletor_datas", "start_date"),
    Output(f"{id_pagina()}_seletor_datas", "end_date"),
    Output(f"{id_pagina()}_periodo_escolhido", "children"),
    Input(f"{id_pagina()}_modal_erro_titulo", "children"),
    State(f"{id_pagina()}_seletor_datas", "start_date"),
    State(f"{id_pagina()}_seletor_datas", "end_date"),
    prevent_initial_call=True,
    running=[(Output(f"{id_pagina()}_botao", "disabled"), True, False)],
)
def top_10_marcas_periodo_atualizar_comparacao(titulo, data_inicio, data_fim):
    if titulo != "":
        raise PreventUpdate

    if not gerenciador.valida_entrada_datas(data_inicio, data_fim):
        raise PreventUpdate

    df_novo = gerenciador.pagina_top_10_marcas_periodo_atualiza_dados_escolhido(
        data_inicio, data_fim
    )

    periodo_novo = uteis_processamento.retorna_periodo(
        data_inicio=data_inicio, data_fim=data_fim
    )

    patch_figura = Patch()

    patch_figura["data"][0]["x"] = df_novo["Marca"].values
    patch_figura["data"][0]["y"] = df_novo["Porcentagem"].values

    return patch_figura, None, None, periodo_novo
