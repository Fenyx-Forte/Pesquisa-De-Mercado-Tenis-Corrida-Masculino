from pandas import DataFrame as pd_DataFrame

from dashboard.processamento import escopo_global, inicializacao_dados
from dashboard.processamento.paginas import (
    processamento_pagina_1,
    processamento_pagina_2,
    processamento_pagina_3,
    processamento_pagina_4,
    processamento_pagina_5,
    processamento_pagina_6,
)


def inicializar_escopo_global() -> None:
    global escopo_aplicacaco

    inicializacao_dados.inicializar_variaveis_ambiente()
    conexao = inicializacao_dados.inicializar_conexao_duckdb()

    inicializacao_dados.configurar_duckdb(conexao)
    inicializacao_dados.inicializar_tabela_dados_completos(conexao)
    inicializacao_dados.inicializar_tabela_dados_mais_recentes(conexao)
    inicializacao_dados.inicializar_macro_dados_completos_por_periodo(conexao)
    inicializacao_dados.inicializar_macro_top_10_marcas_periodo(conexao)
    inicializacao_dados.inicializar_macro_preco_medio_periodo(conexao)

    cabecalho_data_coleta = (
        inicializacao_dados.inicializar_cabecalho_data_coleta(conexao)
    )
    data_coleta_mais_recente = (
        inicializacao_dados.inicializar_data_coleta_mais_recente(conexao)
    )
    data_coleta_mais_antiga = (
        inicializacao_dados.inicializar_data_coleta_mais_antiga(conexao)
    )
    data_6_dias_atras = inicializacao_dados.inicializar_data_6_dias_atras(
        conexao
    )

    periodo_hoje = inicializacao_dados.inicializar_periodo_hoje(
        data_coleta_mais_recente
    )

    periodo_ultima_semana = (
        inicializacao_dados.inicializar_periodo_ultima_semana(
            data_6_dias_atras, data_coleta_mais_recente
        )
    )

    periodo_historico = inicializacao_dados.inicializar_periodo_historico(
        data_coleta_mais_antiga, data_coleta_mais_recente
    )

    df_top_10_marcas_hoje = (
        inicializacao_dados.inicializar_df_top_10_marcas_hoje(
            conexao, data_coleta_mais_recente
        )
    )

    escopo_aplicacaco = escopo_global.EscopoGlobal(
        conexao=conexao,
        cabecalho_data_coleta=cabecalho_data_coleta,
        data_coleta_mais_recente=data_coleta_mais_recente,
        data_6_dias_atras=data_6_dias_atras,
        data_coleta_mais_antiga=data_coleta_mais_antiga,
        periodo_hoje=periodo_hoje,
        periodo_ultima_semana=periodo_ultima_semana,
        periodo_historico=periodo_historico,
        df_top_10_marcas_hoje=df_top_10_marcas_hoje,
    )


def retorna_cabecalho_data_coleta() -> str:
    return escopo_aplicacaco.cabecalho_data_coleta


def retorna_data_coleta_mais_recente() -> str:
    return escopo_aplicacaco.data_coleta_mais_recente


def retorna_data_coleta_mais_antiga() -> str:
    return escopo_aplicacaco.data_coleta_mais_antiga


def retorna_periodo_hoje() -> str:
    return escopo_aplicacaco.periodo_hoje


def retorna_periodo_ultima_semana() -> str:
    return escopo_aplicacaco.periodo_ultima_semana


def retorna_periodo_historico() -> str:
    return escopo_aplicacaco.periodo_historico


def retorna_top_10_marcas_hoje() -> pd_DataFrame:
    return escopo_aplicacaco.df_top_10_marcas_hoje


# Pagina 1
def pagina_1_inicializa_coluna_hoje():
    return processamento_pagina_1.inicializa_coluna_hoje(
        conexao=escopo_aplicacaco.conexao,
        data_coleta_mais_recente=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_1_inicializa_coluna_escolhido():
    return processamento_pagina_1.inicializa_coluna_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
        sufixo="escolhido",
    )


def pagina_1_inicializa_coluna_historico():
    return processamento_pagina_1.inicializa_coluna_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
        sufixo="historico",
    )


def pagina_1_atualiza_coluna_escolhido(data_inicio: str, data_fim: str):
    return processamento_pagina_1.atualiza_coluna_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina 2
def pagina_2_top_10_marcas_atuais():
    return processamento_pagina_2.inicializa_top_10_marcas_atuais(
        conexao=escopo_aplicacaco.conexao,
        data_coleta_mais_recente=escopo_aplicacaco.data_coleta_mais_recente,
        data_6_dias_atras=escopo_aplicacaco.data_6_dias_atras,
        data_coleta_mais_antiga=escopo_aplicacaco.data_coleta_mais_antiga,
        df_hoje=escopo_aplicacaco.df_top_10_marcas_hoje,
    )


def pagina_2_dados_grafico_atualizado(
    dados_grafico_atual: list[dict],
    data_inicio: str,
    data_fim: str,
):
    return processamento_pagina_2.dados_grafico_atualizado(
        conexao=escopo_aplicacaco.conexao,
        dados_grafico_atual=dados_grafico_atual,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina 3
def pagina_3_inicializa_top_10_marcas_escolhido():
    return processamento_pagina_3.df_top_10_marcas_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_3_inicializa_top_10_marcas_historico():
    return processamento_pagina_3.df_top_10_marcas_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_3_atualiza_top_10_marcas_periodo(data_inicio: str, data_fim: str):
    return processamento_pagina_3.df_top_10_marcas_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina 4
def pagina_4_inicializa_dados_hoje() -> list[list[dict]]:
    return processamento_pagina_4.dados_hoje(
        conexao=escopo_aplicacaco.conexao,
    )


def pagina_4_inicializa_dados_escolhido() -> list[list[dict]]:
    return processamento_pagina_4.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_4_inicializa_dados_historico() -> list[list[dict]]:
    return processamento_pagina_4.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_4_atualiza_dados_escolhido(
    data_inicio: str, data_fim: str
) -> list[list[dict]]:
    return processamento_pagina_4.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )
