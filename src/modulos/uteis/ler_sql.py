from os import getenv

from duckdb import DuckDBPyConnection, DuckDBPyRelation, connect, execute, sql
from loguru import logger
from polars import DataFrame


def ler_conteudo_query(caminho_query: str) -> str:
    query = ""
    with open(caminho_query, "r") as file:
        query = file.read()

    return query


def conexao_banco_de_dados() -> DuckDBPyConnection:
    query_conexao = f"""
        INSTALL postgres;
        LOAD postgres;
        ATTACH '{getenv("DATABASE_URL")}' AS db (TYPE POSTGRES);
    """

    return execute(query_conexao)


def conexao_banco_de_dados_apenas_leitura() -> DuckDBPyConnection:
    query_conexao = f"""
        INSTALL postgres;
        LOAD postgres;
        ATTACH '{getenv("DATABASE_URL")}' AS db (TYPE POSTGRES, READ_ONLY);
    """

    return execute(query_conexao)


def query_banco_de_dados(query: str) -> DataFrame:
    df: DataFrame = None

    with conexao_banco_de_dados() as conexao:
        logger.info("Conexao criada")
        df = conexao.sql(query).pl()
        logger.info("Dados obtidos")

    logger.info("Conexao encerrada")
    return df


def query_banco_de_dados_apenas_leitura(query: str) -> DataFrame:
    df: DataFrame = None

    with conexao_banco_de_dados_apenas_leitura() as conexao:
        # logger.info("Conexao criada")
        df = conexao.sql(query).pl()
        # logger.info("Dados obtidos")

    # logger.info("Conexao encerrada")
    return df


def query_pl_para_pl(query: str, df: DataFrame) -> DataFrame:
    with connect() as conexao:
        df_novo = conexao.sql(query).pl()

    return df_novo


def query_pl_para_pl_com_parametro(
    query: str, parametros: dict, df: DataFrame
) -> DataFrame:
    with connect() as conexao:
        df_novo = conexao.execute(query, parametros).pl()

    return df_novo


def query_duckbdb_para_pl(query: str, df: DuckDBPyRelation) -> DataFrame:
    return sql(query).pl()


def query_duckdb_para_duckdb(
    query: str, df: DuckDBPyRelation
) -> DuckDBPyRelation:
    return sql(query)
