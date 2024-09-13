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
    inicializacao_dados.inicializar_macro_top_10_marcas_atuais(conexao)
    inicializacao_dados.inicializar_macro_top_10_marcas_periodo(conexao)
    inicializacao_dados.inicializar_macro_top_10_marcas_historico(conexao)

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

    escopo_aplicacaco = escopo_global.EscopoGlobal(
        conexao=conexao,
        cabecalho_data_coleta=cabecalho_data_coleta,
        data_coleta_mais_recente=data_coleta_mais_recente,
        data_6_dias_atras=data_6_dias_atras,
        data_coleta_mais_antiga=data_coleta_mais_antiga,
    )


def retorna_cabecalho_data_coleta() -> str:
    return escopo_aplicacaco.cabecalho_data_coleta


def retorna_data_coleta_mais_recente() -> str:
    return escopo_aplicacaco.data_coleta_mais_recente


def retorna_data_coleta_mais_antiga() -> str:
    return escopo_aplicacaco.data_coleta_mais_antiga


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
    )


def pagina_2_grafico_comparacao_top_10(
    dados_grafico_atual: list[dict],
    data_inicio: str,
    data_fim: str,
):
    return processamento_pagina_2.dados_grafico_comparacao_top_10(
        conexao=escopo_aplicacaco.conexao,
        dados_grafico_atual=dados_grafico_atual,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina 3
def pagina_3_top_10_marcas_historico():
    return processamento_pagina_3.inicializa_top_10_marcas_historico(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_3_top_10_marcas_periodo(data_inicio: str, data_fim: str):
    return processamento_pagina_3.top_10_marcas_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina 6
def pagina_6_inicializa_tabela() -> list[dict]:
    return processamento_pagina_6.inicializa_tabela(
        conexao=escopo_aplicacaco.conexao,
    )
