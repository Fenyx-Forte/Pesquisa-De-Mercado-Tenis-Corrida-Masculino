"""Módulo responsável por validar os dados de entrada e saida utilizando o contrato de dados."""

import pandera.polars as pa
import polars as pl
from loguru import logger

from modulos.contrato_de_dados import contrato_entrada, contrato_saida


class ValidacaoError(Exception):
    """Erro de validação de dados."""


def validar_dados_entrada(df: pl.DataFrame) -> None:
    """Valida os dados de entrada utilizando o contrato de dados.

    Args:
        df (pl.DataFrame): Dados de entrada.

    Raises:
        ValidacaoError: Se os dados não forem válidos.
    """
    logger.info("Validando dados de entrada...")
    try:
        contrato_entrada.TenisCorridaEntrada.validate(df)
        logger.info("Dados validos")
    except pa.errors.SchemaError as exc:
        logger.error(exc)
        mensagem_erro = "Dados de entrada não são válidos!"
        raise ValidacaoError(mensagem_erro) from None


def validar_dados_saida(df: pl.DataFrame) -> None:
    """Valida os dados de saída utilizando o contrato de dados.

    Args:
        df (pl.DataFrame): Dados de entrada.

    Raises:
        ValidacaoError: Se os dados não forem válidos.
    """
    logger.info("Validando dados de saida...")
    try:
        contrato_saida.TenisCorridaSaida.validate(df)
        logger.info("Dados validos")
    except pa.errors.SchemaError as exc:
        logger.error(exc)
        mensagem_erro = "Dados de saída não são válidos!"
        raise ValidacaoError(mensagem_erro) from None
