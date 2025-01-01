"""Módulo de configuração do polars."""

import polars as pl


def configuracao_polars(caminho_arquivo: str) -> None:
    """Carrega a configuração do polars.

    Args:
        caminho_arquivo (str): Caminho para o arquivo de configuração do polars.
    """
    pl.Config.load_from_file(caminho_arquivo)
