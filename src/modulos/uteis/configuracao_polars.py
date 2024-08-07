import polars as pl


def configuracao_polars(caminho_arquivo: str) -> None:
    pl.Config.load_from_file(caminho_arquivo)
