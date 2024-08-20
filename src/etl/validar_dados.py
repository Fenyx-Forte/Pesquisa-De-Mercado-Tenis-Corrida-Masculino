import pandera.polars as pa
import polars as pl
from loguru import logger
from modulos.contrato_de_dados import contrato_entrada, contrato_saida


def validar_dados_entrada(df: pl.DataFrame) -> None:
    logger.info("Validando dados de entrada...")
    try:
        contrato_entrada.MercadoLivreEntrada.validate(df)
        logger.info("Dados validos")
    except pa.errors.SchemaError as exc:
        logger.error(exc)
        raise pa.errors.SchemaError("Dados de entrada nao sao validos!")


def validar_dados_saida(df: pl.DataFrame) -> None:
    logger.info("Validando dados de saida...")
    try:
        contrato_saida.MercadoLivreSaida.validate(df)
        logger.info("Dados validos")
    except pa.errors.SchemaError as exc:
        logger.error(exc)
        raise pa.errors.SchemaError("Dados de saida nao sao validos!")
