from duckdb import DuckDBPyConnection

from dashboard.processamento.queries import queries_promocoes


def dados_hoje(conexao: DuckDBPyConnection) -> list[dict]:
    query = queries_promocoes.query_promocao_hoje()

    return conexao.sql(query).df().to_dict(orient="records")


def dados_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
) -> list[dict]:
    query = queries_promocoes.query_promocao_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return conexao.execute(query, parametros).df().to_dict(orient="records")
