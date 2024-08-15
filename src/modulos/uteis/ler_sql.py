import duckdb


def ler_conteudo_query(caminho_query: str) -> str:
    query = ""
    with open(caminho_query, "r") as file:
        query = file.read()

    return query


def query(query_path: str) -> duckdb.DuckDBPyRelation:
    query_content = ler_conteudo_query(query_path)

    return duckdb.sql(query_content)
