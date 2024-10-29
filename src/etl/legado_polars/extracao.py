import polars as pl
from loguru import logger


def extrair_dados_json(caminho_arquivo: str) -> pl.DataFrame:
    logger.info("Extraindo dados json...")
    return pl.read_json(caminho_arquivo)
