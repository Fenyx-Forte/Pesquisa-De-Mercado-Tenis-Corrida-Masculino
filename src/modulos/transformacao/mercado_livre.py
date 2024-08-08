from datetime import datetime

import polars as pl


def tratar_marca() -> pl.Expr:
    coluna_tratada = pl.col("marca").fill_null("GENERICA").str.to_uppercase()

    return coluna_tratada


def tratar_produto() -> pl.Expr:
    coluna_tratada = pl.col("produto").str.to_uppercase()

    return coluna_tratada


def tratar_nota_avaliacao() -> pl.Expr:
    coluna_tratada = pl.col("nota_avaliacao").cast(pl.Float32)

    return coluna_tratada


def tratar_num_avaliacoes() -> pl.Expr:
    coluna_tratada = (
        pl.col("num_avaliacoes").str.strip_chars("()").cast(pl.Int32)
    )

    return coluna_tratada


def reduzir_armazenamento_nota_avaliacao() -> pl.Expr:
    coluna_tratada = pl.col("nota_avaliacao").cast(pl.Float32)

    return coluna_tratada


def adiciona_fonte_dados(fonte: str) -> pl.Expr:
    return pl.lit(fonte).alias("_fonte")


def adiciona_data_coleta(data: datetime) -> pl.Expr:
    ano = data.year
    mes = data.month
    dia = data.day
    hora = data.hour
    minuto = data.minute
    segundo = data.second
    return pl.datetime(ano, mes, dia, hora, minuto, segundo).alias(
        "_data_coleta"
    )


def adiciona_preco_completo(
    col_preco_reais: str, col_preco_centavos: str, nome_coluna_nova: str
) -> pl.Expr:
    coluna_nova = (
        pl.when(
            (pl.col(col_preco_reais).is_not_null())
            & (pl.col(col_preco_centavos).is_not_null())
        )
        .then(
            pl.col(col_preco_reais).str.replace(".", "", literal=True)
            + "."
            + pl.col(col_preco_centavos)
        )
        .otherwise(
            pl.when(pl.col(col_preco_centavos).is_null())
            .then(pl.col(col_preco_reais).str.replace(".", "", literal=True))
            .otherwise(None)
        )
        .cast(pl.Float32)
        .alias(nome_coluna_nova)
    )

    return coluna_nova


def adicionar_promocao() -> pl.Expr:
    return pl.col("preco_velho").is_null().alias("promocao")


def adicionar_percentual_promocao() -> pl.Expr:
    coluna_nova = (
        pl.when(pl.col("preco_velho").is_not_null())
        .then(
            100
            * (pl.col("preco_velho") - pl.col("preco_atual"))
            / pl.col("preco_velho")
        )
        .otherwise(0)
        .alias("percentual_promocao")
    )

    return coluna_nova
