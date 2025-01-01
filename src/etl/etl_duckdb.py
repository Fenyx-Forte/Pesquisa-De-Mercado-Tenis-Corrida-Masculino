"""Pipeline para extração, processamento e salvamento de dados."""

from duckdb import connect
from loguru import logger

from etl import (
    duckdb_local,
    extracao_sql,
    salvar_sql,
    validar_dados,
)
from modulos.uteis import funcoes_sql, meu_tempo, minhas_queries


def pipeline() -> None:
    """Pipeline para extração, processamento e salvamento de dados."""
    # Extracao
    horario = meu_tempo.data_agora_string()

    nome_arquivo = (
        f"tenis_corrida_{meu_tempo.data_agora_simplificada_com_underline()}"
    )

    caminho_json = f"../dados/nao_processados/{nome_arquivo}.json"

    # Verificacao
    arquivo_ja_foi_salvo = duckdb_local.verifica_se_arquivo_ja_foi_salvo(
        nome_arquivo,
    )

    if arquivo_ja_foi_salvo:
        logger.info("Arquivo ja foi salvo no banco de dados!")
        return

    conexao = connect(":memory:")

    df_entrada = extracao_sql.extracao_json(caminho_json, conexao)

    # Validacao
    query_entrada = minhas_queries.cast_polars_entrada()

    validar_dados.validar_dados_entrada(
        funcoes_sql.query_duckbdb_para_pl(query_entrada, df_entrada, conexao),
    )

    # Transformacao
    caminho_query = "../sql/transformacao/tratamento_dados.sql"

    query_transfomacao = funcoes_sql.ler_conteudo_query(caminho_query)

    df_saida = funcoes_sql.query_duckdb_para_duckdb(
        query_transfomacao,
        df_entrada,
        conexao,
    )

    # Validacao
    query_saida = minhas_queries.cast_polars_saida()

    validar_dados.validar_dados_saida(
        funcoes_sql.query_duckbdb_para_pl(query_saida, df_saida, conexao),
    )

    # Salvar
    query_insercao = funcoes_sql.ler_conteudo_query(
        "../sql/dml/inserir_dados.sql",
    )

    salvar_sql.salvar_dados(
        query_insercao,
        df_saida,
        conexao,
        nome_arquivo,
        horario,
    )

    conexao.close()
