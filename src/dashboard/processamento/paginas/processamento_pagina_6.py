from duckdb import DuckDBPyConnection


def query_tabela() -> str:
    query = """
    SELECT
        marca
        , produto
        , preco_atual
        , promocao
        , percentual_promocao
    FROM
        dados_mais_recentes;
    """

    return query


def inicializa_tabela(conexao: DuckDBPyConnection) -> list[dict]:
    query = query_tabela()

    return conexao.sql(query).df().to_dict("records")
