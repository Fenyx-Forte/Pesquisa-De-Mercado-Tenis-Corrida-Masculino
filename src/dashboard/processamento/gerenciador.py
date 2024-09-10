from dashboard.processamento import escopo_global, inicializacao_dados
from dashboard.processamento.paginas import (
    processamento_pagina_1,
    processamento_pagina_2,
    processamento_pagina_3,
    processamento_pagina_4,
)


def inicializar_escopo_global() -> None:
    global escopo_aplicacaco

    inicializacao_dados.inicializar_variaveis_ambiente()
    conexao = inicializacao_dados.inicializar_conexao_duckdb()

    inicializacao_dados.configurar_duckdb(conexao)
    inicializacao_dados.inicializar_tabela_dados_completos(conexao)
    inicializacao_dados.inicializar_tabela_dados_mais_recentes(conexao)

    cabecalho_data_coleta = (
        inicializacao_dados.inicializar_cabecalho_data_coleta(conexao)
    )
    data_coleta_mais_recente = (
        inicializacao_dados.inicializar_data_coleta_mais_recente(conexao)
    )
    data_coleta_mais_antiga = (
        inicializacao_dados.inicializar_data_coleta_mais_antiga(conexao)
    )

    escopo_aplicacaco = escopo_global.EscopoGlobal(
        conexao,
        cabecalho_data_coleta,
        data_coleta_mais_recente,
        data_coleta_mais_antiga,
    )


def retorna_cabecalho_data_coleta() -> str:
    return escopo_aplicacaco.cabecalho_data_coleta


def retorna_data_coleta_mais_recente() -> str:
    return escopo_aplicacaco.data_coleta_mais_recente


def retorna_data_coleta_mais_antiga() -> str:
    return escopo_aplicacaco.data_coleta_mais_antiga


# Pagina 1
def pagina_1_top_10_marcas_atual():
    return processamento_pagina_1.inicializa_top_10_marcas_atual(
        escopo_aplicacaco.conexao, escopo_aplicacaco.data_coleta_mais_recente
    )


def pagina_1_grafico_comparacao_top_10(
    dados_grafico_atual: list[dict],
    data_inicio: str,
    data_fim: str,
):
    return processamento_pagina_1.dados_grafico_comparacao_top_10(
        escopo_aplicacaco.conexao,
        dados_grafico_atual,
        data_inicio,
        data_fim,
    )


# Pagina 4
def pagina_4_inicializa_tabela() -> list[dict]:
    return processamento_pagina_4.inicializa_tabela(escopo_aplicacaco.conexao)
