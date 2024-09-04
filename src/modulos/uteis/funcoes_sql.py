from os import getenv

from duckdb import DuckDBPyConnection, DuckDBPyRelation, connect
from polars import DataFrame


def ErroConexao(Exception):
    pass


def ler_conteudo_query(caminho_query: str) -> str:
    query = ""
    with open(caminho_query, "r") as file:
        query = file.read()

    return query


def string_conexao_banco_de_dados_webscraping() -> str:
    query_conexao = f"""
        ATTACH '{getenv("DATABASE_URL_WEBSCRAPING")}' AS db (TYPE POSTGRES);
    """

    return query_conexao


def string_conexao_banco_de_dados_dashboard() -> str:
    query_conexao = f"""
        ATTACH '{getenv("DATABASE_URL_DASHBOARD")}' AS db (TYPE POSTGRES, READ_ONLY);
    """

    return query_conexao


def conexao_banco_de_dados_webscraping(conexao: DuckDBPyConnection) -> None:
    try:
        conexao.sql(string_conexao_banco_de_dados_webscraping())
    except Exception:
        raise ErroConexao(
            "Aconteceu algum erro ao tentar estabelecer uma conexao com o banco de dados"
        )


def conexao_banco_de_dados_dashboard(conexao: DuckDBPyConnection) -> None:
    try:
        conexao.sql(string_conexao_banco_de_dados_dashboard())
    except Exception:
        raise ErroConexao(
            "Aconteceu algum erro ao tentar estabelecer uma conexao com o banco de dados"
        )


def query_pl_para_pl(query: str, df: DataFrame) -> DataFrame:
    with connect(":memory:") as conexao:
        df_novo = conexao.sql(query).pl()

    return df_novo


def query_pl_para_pl_com_parametro(
    query: str, parametros: dict, df: DataFrame
) -> DataFrame:
    with connect(":memory:") as conexao:
        df_novo = conexao.execute(query, parametros).pl()

    return df_novo


def query_duckbdb_para_pl(
    query: str, df: DuckDBPyRelation, conexao: DuckDBPyConnection
) -> DataFrame:
    return conexao.sql(query).pl()


def query_duckdb_para_duckdb(
    query: str, df: DuckDBPyRelation, conexao: DuckDBPyConnection
) -> DuckDBPyRelation:
    return conexao.sql(query)
