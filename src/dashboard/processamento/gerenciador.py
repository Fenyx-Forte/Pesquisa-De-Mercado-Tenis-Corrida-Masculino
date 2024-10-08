from pandas import DataFrame as pd_DataFrame

from dashboard.processamento import escopo_global, inicializacao_dados
from dashboard.processamento.paginas import (
    processamento_faixa_preco,
    processamento_kpis,
    processamento_preco_medio,
    processamento_promocoes,
    processamento_satisfacao,
    processamento_top_10_marcas_atuais,
    processamento_top_10_marcas_periodo,
)


def inicializar_escopo_global() -> None:
    global escopo_aplicacaco

    inicializacao_dados.inicializar_variaveis_ambiente()
    conexao = inicializacao_dados.inicializar_conexao_duckdb()

    inicializacao_dados.configurar_duckdb(conexao)
    inicializacao_dados.inicializar_tabela_dados_completos(conexao)
    inicializacao_dados.inicializar_tabela_dados_mais_recentes(conexao)
    inicializacao_dados.inicializar_macro_dados_completos_por_periodo(conexao)
    inicializacao_dados.inicializar_macro_kpis_periodo(conexao)
    inicializacao_dados.inicializar_macro_top_10_marcas_periodo(conexao)
    inicializacao_dados.inicializar_macro_preco_medio_periodo(conexao)
    inicializacao_dados.inicializar_macro_faixa_preco_periodo(conexao)
    inicializacao_dados.inicializar_macro_media_avaliacoes_periodo(conexao)
    inicializacao_dados.inicializar_macro_media_promocoes_periodo(conexao)

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


# Pagina KPIs
def pagina_kpis_dados_hoje() -> dict[str, str]:
    return processamento_kpis.dados_hoje(
        conexao=escopo_aplicacaco.conexao,
    )


def pagina_kpis_dados_ultima_semana() -> dict[str, str]:
    return processamento_kpis.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_kpis_dados_historico() -> dict[str, str]:
    return processamento_kpis.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_kpis_atualiza_dados_escolhido(
    data_inicio: str,
    data_fim: str,
) -> dict[str, str]:
    return processamento_kpis.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina Top 10 Marcas Atuais
def pagina_top_10_marcas_atuais_dados_grafico() -> pd_DataFrame:
    return processamento_top_10_marcas_atuais.inicializa_top_10_marcas_atuais(
        conexao=escopo_aplicacaco.conexao,
        data_coleta_mais_recente=escopo_aplicacaco.data_coleta_mais_recente,
        data_6_dias_atras=escopo_aplicacaco.data_6_dias_atras,
        data_coleta_mais_antiga=escopo_aplicacaco.data_coleta_mais_antiga,
        df_hoje=escopo_aplicacaco.df_top_10_marcas_hoje,
    )


def pagina_top_10_marcas_atuais_atualizar_dados_grafico(
    dados_grafico_atual: dict[str, list[dict]],
    data_inicio: str,
    data_fim: str,
) -> pd_DataFrame:
    return processamento_top_10_marcas_atuais.dados_grafico_atualizado(
        conexao=escopo_aplicacaco.conexao,
        dados_grafico_atual=dados_grafico_atual,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina Top 10 Marcas Periodo
def pagina_top_10_marcas_periodo_dados_hoje():
    return retorna_top_10_marcas_hoje()


def pagina_top_10_marcas_periodo_dados_ultima_semana():
    return processamento_top_10_marcas_periodo.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_top_10_marcas_periodo_dados_historico():
    return processamento_top_10_marcas_periodo.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_top_10_marcas_periodo_atualiza_dados_escolhido(
    data_inicio: str,
    data_fim: str,
):
    return processamento_top_10_marcas_periodo.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina Preco Medio
def pagina_preco_medio_dados_hoje() -> dict[str, list[dict]]:
    return processamento_preco_medio.dados_hoje(
        conexao=escopo_aplicacaco.conexao,
    )


def pagina_preco_medio_dados_ultima_semana() -> dict[str, list[dict]]:
    return processamento_preco_medio.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_preco_medio_dados_historico() -> dict[str, list[dict]]:
    return processamento_preco_medio.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_preco_medio_atualiza_dados_escolhido(
    data_inicio: str,
    data_fim: str,
) -> dict[str, list[dict]]:
    return processamento_preco_medio.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina Faixa Preco
def pagina_faixa_preco_dados_hoje() -> dict[str, list[dict]]:
    return processamento_faixa_preco.dados_hoje(
        conexao=escopo_aplicacaco.conexao,
    )


def pagina_faixa_preco_dados_ultima_semana() -> dict[str, list[dict]]:
    return processamento_faixa_preco.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_faixa_preco_dados_historico() -> dict[str, list[dict]]:
    return processamento_faixa_preco.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_faixa_preco_atualiza_dados_escolhido(
    data_inicio: str, data_fim: str
) -> dict[str, list[dict]]:
    return processamento_faixa_preco.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina Satisfacao
def pagina_satisfacao_dados_hoje() -> dict[str, list[dict]]:
    return processamento_satisfacao.dados_hoje(
        conexao=escopo_aplicacaco.conexao,
    )


def pagina_satisfacao_dados_ultima_semana() -> dict[str, list[dict]]:
    return processamento_satisfacao.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_satisfacao_dados_historico() -> dict[str, list[dict]]:
    return processamento_satisfacao.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_satisfacao_atualiza_dados_escolhido(
    data_inicio: str, data_fim: str
) -> dict[str, list[dict]]:
    return processamento_satisfacao.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


# Pagina Promocoes
def pagina_promocoes_dados_hoje() -> list[dict]:
    return processamento_promocoes.dados_hoje(
        conexao=escopo_aplicacaco.conexao,
    )


def pagina_promocoes_dados_ultima_semana() -> list[dict]:
    return processamento_promocoes.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_6_dias_atras,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_promocoes_dados_historico() -> list[dict]:
    return processamento_promocoes.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=escopo_aplicacaco.data_coleta_mais_antiga,
        data_fim=escopo_aplicacaco.data_coleta_mais_recente,
    )


def pagina_promocoes_atualiza_dados_escolhido(
    data_inicio: str, data_fim: str
) -> list[dict]:
    return processamento_promocoes.dados_periodo(
        conexao=escopo_aplicacaco.conexao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )
