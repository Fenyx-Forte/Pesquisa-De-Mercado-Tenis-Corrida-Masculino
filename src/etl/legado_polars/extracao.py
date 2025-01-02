"""Módulo que extrai os dados do webscraping a partir de um arquivo json."""

import polars as pl
from loguru import logger


def extrair_dados_json(caminho_arquivo: str) -> pl.DataFrame:
    """Extrai os dados do arquivo json e retorna um dataframe polars.

    Args:
        caminho_arquivo (str): Caminho para o arquivo json.

    Returns:
        pl.DataFrame: Dados extraidos do arquivo json.
    """
    logger.info("Extraindo dados json...")
    return pl.read_json(caminho_arquivo)
