from duckdb import DuckDBPyConnection, connect


def conexao_duckdb_local() -> DuckDBPyConnection:
    caminho = "../dados/duckdb_database.db"

    conexao = connect(
        database=caminho,
        read_only=True,
    )

    return conexao
