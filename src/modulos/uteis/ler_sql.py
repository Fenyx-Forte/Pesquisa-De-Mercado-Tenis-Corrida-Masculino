import os

import duckdb
from loguru import logger


def ler_conteudo_query(caminho_query: str) -> str:
    query = ""
    with open(caminho_query, "r") as file:
        query = file.read()

    return query


def conexao_banco_de_dados() -> duckdb.DuckDBPyConnection:
    query_conexao = f"""
        INSTALL postgres;
        LOAD postgres;
        ATTACH '{os.getenv("DATABASE_URL")}' AS db (TYPE POSTGRES);
    """

    return duckdb.execute(query_conexao)


def query_banco_de_dados(caminho_query: str) -> duckdb.DuckDBPyRelation:
    query = ler_conteudo_query(caminho_query)

    df: duckdb.DuckDBPyRelation = None

    with conexao_banco_de_dados() as conexao:
        logger.info("Conexao criada")
        df = conexao.sql(query)
        logger.info("Dados obtidos")

    logger.info("Conexao encerrada")
    return df


def query_df(
    caminho_query: str, df: duckdb.DuckDBPyRelation
) -> duckdb.DuckDBPyRelation:
    query = ler_conteudo_query(caminho_query)

    return duckdb.sql(query)
