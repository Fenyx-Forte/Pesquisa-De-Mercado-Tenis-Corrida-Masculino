"""Módulo de configuração do polars."""

import polars as pl


def configuracao_polars(caminho_arquivo: str) -> None:
    """Carrega a configuração do polars."""
    pl.Config.load_from_file(caminho_arquivo)
