from duckdb import DuckDBPyConnection, DuckDBPyRelation
from loguru import logger


def extracao_json(
    caminho_json: str, conexao: DuckDBPyConnection
) -> DuckDBPyRelation:
    logger.info("Extraindo dados...")

    df = conexao.read_json(caminho_json)

    logger.info("Dados extraidos")

    return df
