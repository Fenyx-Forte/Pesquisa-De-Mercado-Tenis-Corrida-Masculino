import polars as pl


def configuracao_polars() -> None:
    pl.Config.load_from_file("./configuracao/polars.json")
