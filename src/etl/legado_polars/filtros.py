import polars as pl
from loguru import logger


def remover_valores_null(lf: pl.LazyFrame) -> pl.LazyFrame:
    logger.info("Removendo valores null da coluna 'preco_atual'")
    return lf.drop_nulls("preco_atual")


def remover_valores_duplicados(lf: pl.LazyFrame) -> pl.LazyFrame:
    logger.info("Removendo linhas duplicadas")
    return lf.unique()
