import polars as pl


def tratar_coluna_string(nome_coluna: str) -> pl.Expr:
    coluna_tratada = (
        pl.col(nome_coluna)
        .str.to_uppercase()
        .str.replace_all(r"[ÁÀÂÃÄÅ]", "A")
        .str.replace_all(r"[ÉÈÊË]", "E")
        .str.replace_all(r"[ÍÌÎÏ]", "I")
        .str.replace_all(r"[ÓÒÔÕÖ]", "O")
        .str.replace_all(r"[ÚÙÛÜ]", "U")
        .str.replace_all("Ç", "C", literal=True)
        .str.replace_all(r"[^A-Z0-9 ]", " ")
        .str.replace_all(r"\s+", " ")
        .str.strip_chars()
    )

    return coluna_tratada


def tratar_marca() -> pl.Expr:
    coluna_tratada = tratar_coluna_string("marca").fill_null("GENERICA")

    return coluna_tratada


def tratar_produto() -> pl.Expr:
    coluna_tratada = tratar_coluna_string("produto").fill_null(
        "PRODUTO SEM NOME"
    )

    return coluna_tratada


def tratar_preco_velho_reais() -> pl.Expr:
    coluna_tratada = pl.col("preco_velho_reais").str.replace(
        ".", "", literal=True
    )

    return coluna_tratada


def tratar_preco_atual_reais() -> pl.Expr:
    coluna_tratada = pl.col("preco_atual_reais").str.replace(
        ".", "", literal=True
    )

    return coluna_tratada


def tratar_nota_avaliacao() -> pl.Expr:
    coluna_tratada = pl.col("nota_avaliacao").fill_null(0).cast(pl.Float32)

    return coluna_tratada


def tratar_num_avaliacoes() -> pl.Expr:
    coluna_tratada = (
        pl.col("num_avaliacoes")
        .str.strip_chars("()")
        .fill_null(0)
        .cast(pl.Int32)
    )

    return coluna_tratada


def tratar_fonte() -> pl.Expr:
    coluna_tratada = pl.col("_fonte").cast(pl.Categorical)

    return coluna_tratada


def tratar_site() -> pl.Expr:
    coluna_tratada = pl.col("_site").cast(pl.Categorical)

    return coluna_tratada


def tratar_data_coleta() -> pl.Expr:
    coluna_tratada = pl.col("_data_coleta").str.to_datetime()

    return coluna_tratada


def tratar_pagina() -> pl.Expr:
    coluna_tratada = pl.col("_pagina").cast(pl.Int8)

    return coluna_tratada


def tratar_ordem() -> pl.Expr:
    coluna_tratada = pl.col("_ordem").cast(pl.Int8)

    return coluna_tratada


def adiciona_preco_completo(
    col_preco_reais: str, col_preco_centavos: str, nome_coluna_nova: str
) -> pl.Expr:
    coluna_nova = (
        pl.when(
            pl.col(col_preco_reais).is_not_null()
            & pl.col(col_preco_centavos).is_not_null()
        )
        .then(pl.col(col_preco_reais) + "." + pl.col(col_preco_centavos))
        .otherwise(
            pl.when(pl.col(col_preco_centavos).is_null())
            .then(pl.col(col_preco_reais))
            .otherwise(None)
        )
        .cast(pl.Float32)
        .alias(nome_coluna_nova)
    )

    return coluna_nova


def adicionar_preco_velho_completo() -> pl.Expr:
    coluna_nova = adiciona_preco_completo(
        col_preco_reais="preco_velho_reais",
        col_preco_centavos="preco_velho_centavos",
        nome_coluna_nova="preco_velho",
    )

    return coluna_nova


def adicionar_preco_atual_completo() -> pl.Expr:
    coluna_nova = adiciona_preco_completo(
        col_preco_reais="preco_atual_reais",
        col_preco_centavos="preco_atual_centavos",
        nome_coluna_nova="preco_atual",
    )

    return coluna_nova


def tratar_preco_velho() -> pl.Expr:
    coluna_tradada = pl.col("preco_velho").fill_null(pl.col("preco_atual"))

    return coluna_tradada


def adicionar_promocao() -> pl.Expr:
    coluna_nova = pl.col("preco_velho").is_not_null().alias("promocao")

    return coluna_nova


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
