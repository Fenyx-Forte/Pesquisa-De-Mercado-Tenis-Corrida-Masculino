import os

import duckdb
import polars as pl
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


def conexao_banco_de_dados_apenas_leitura() -> duckdb.DuckDBPyConnection:
    query_conexao = f"""
        INSTALL postgres;
        LOAD postgres;
        ATTACH '{os.getenv("DATABASE_URL")}' AS db (TYPE POSTGRES, READ_ONLY);
    """

    return duckdb.execute(query_conexao)


def query_banco_de_dados(caminho_query: str) -> pl.DataFrame:
    query = ler_conteudo_query(caminho_query)

    df: pl.DataFrame = None

    with conexao_banco_de_dados() as conexao:
        logger.info("Conexao criada")
        df = conexao.sql(query).pl()
        logger.info("Dados obtidos")

    logger.info("Conexao encerrada")
    return df


def query_banco_de_dados_apenas_leitura(
    caminho_query: str,
) -> pl.DataFrame:
    query = ler_conteudo_query(caminho_query)

    df: pl.DataFrame = None

    with conexao_banco_de_dados_apenas_leitura() as conexao:
        # logger.info("Conexao criada")
        df = conexao.sql(query).pl()
        # logger.info("Dados obtidos")

    # logger.info("Conexao encerrada")
    return df


def query_df(
    caminho_query: str, df: duckdb.DuckDBPyRelation | pl.DataFrame
) -> pl.DataFrame:
    query = ler_conteudo_query(caminho_query)

    with duckdb.connect() as conexao:
        df_novo = conexao.sql(query).pl()

    return df_novo


def query_df_direto(
    query: str, df: duckdb.DuckDBPyRelation | pl.DataFrame
) -> pl.DataFrame:
    with duckdb.connect() as conexao:
        df_novo = conexao.sql(query).pl()

    return df_novo


def query_df_com_parametros(
    query: str, parametros: dict, df: duckdb.DuckDBPyRelation | pl.DataFrame
) -> pl.DataFrame:
    with duckdb.connect() as conexao:
        df_novo = conexao.execute(query, parametros).pl()

    return df_novo
