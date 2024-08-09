import duckdb
import pandas as pd


def ler_conteudo_query(caminho_query: str) -> str:
    query = ""
    with open(caminho_query, "r") as file:
        query = file.read()

    return query


def ler_query(query_path: str) -> pd.DataFrame:
    query_content = ler_conteudo_query(query_path)

    pl_df = duckdb.sql(query_content).df()

    return pl_df
