import duckdb
from loguru import logger


def transformacao(
    query: str, df: duckdb.DuckDBPyRelation
) -> duckdb.DuckDBPyRelation:
    logger.info("Realizando transformacoes...")

    df = duckdb.sql(query)

    logger.info("Transformacoes realizadas")

    return df
