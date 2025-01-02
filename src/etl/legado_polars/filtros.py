"""Módulo que contém funções auxiliares para filtrar os dados do webscraping."""

import polars as pl
from loguru import logger


def remover_valores_null(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Remove linhas com valores nulos da coluna 'preco_atual'.

    Args:
        lf (pl.LazyFrame): DataFrame com os dados do webscraping.

    Returns:
        pl.LazyFrame: DataFrame sem linhas com valores nulos.
    """
    logger.info("Removendo valores null da coluna 'preco_atual'")
    return lf.drop_nulls("preco_atual")


def remover_valores_duplicados(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Remove linhas duplicadas da coluna 'preco_atual'.

    Args:
        lf (pl.LazyFrame): DataFrame com os dados do webscraping.

    Returns:
        pl.LazyFrame: DataFrame sem linhas duplicadas.
    """
    logger.info("Removendo linhas duplicadas")
    return lf.unique()
