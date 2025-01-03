"""Módulo usado para criar a conexão com o duckdb local, que contém os dados usados no dashboard."""

from duckdb import DuckDBPyConnection, connect


def conexao_duckdb_local() -> DuckDBPyConnection:
    """Conecta a um banco de dados DuckDB local.

    Args:
        caminho (str): Caminho do arquivo do banco de dados.

    Returns:
        DuckDBPyConnection: Conexão ao banco de dados DuckDB.
    """
    caminho = "../dados/duckdb_database.db"

    return connect(
        database=caminho,
        read_only=True,
    )
