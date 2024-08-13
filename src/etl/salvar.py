import polars as pl
from loguru import logger


def salvar_dados_parquet(caminho_arquivo: str, df: pl.DataFrame) -> None:
    logger.info("Salvando dados em parquet...")
    df.write_parquet(caminho_arquivo)
    logger.info("Dados salvos!")
