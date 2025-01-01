"""Módulo que extrai dados de um arquivo JSON usando DuckDB."""

from duckdb import DuckDBPyConnection, DuckDBPyRelation
from loguru import logger


def extracao_json(
    caminho_json: str,
    conexao: DuckDBPyConnection,
) -> DuckDBPyRelation:
    """Extrai dados de um arquivo JSON.

    Args:
        caminho_json (str): Caminho para o arquivo JSON.
        conexao (DuckDBPyConnection): Conexão com o banco de dados.

    Returns:
        DuckDBPyRelation: Dados extraídos.
    """
    logger.info("Extraindo dados...")

    df_entrada = conexao.read_json(caminho_json)

    logger.info("Dados extraidos")

    return df_entrada
