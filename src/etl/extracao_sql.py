import duckdb
from loguru import logger


def extracao_json(caminho_json: str) -> duckdb.DuckDBPyRelation:
    logger.info("Extraindo dados...")

    df = duckdb.read_json(caminho_json)

    logger.info("Dados extraidos")

    return df
