import duckdb
import polars as pl


def ler_conteudo_query(caminho_query: str) -> str:
    query = ""
    with open(caminho_query, "r") as file:
        query = file.read()

    return query


def ler_query(query_path: str) -> pl.DataFrame:
    query_content = ler_conteudo_query(query_path)

    return duckdb.sql(query_content).pl()
