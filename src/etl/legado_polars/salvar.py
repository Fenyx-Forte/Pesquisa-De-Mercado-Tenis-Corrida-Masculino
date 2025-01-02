"""Módulo que salva os dados tratados do Webscraping em um arquivo parquet."""

import polars as pl
from loguru import logger


def salvar_dados_parquet(caminho_arquivo: str, df: pl.DataFrame) -> None:
    """Salva os dados tratados do Webscraping em um arquivo parquet.

    Args:
        caminho_arquivo (str): Caminho para o arquivo parquet.
        df (pl.DataFrame): Dados tratados.
    """
    logger.info("Salvando dados em parquet...")
    df.write_parquet(caminho_arquivo)
    logger.info("Dados salvos!")
