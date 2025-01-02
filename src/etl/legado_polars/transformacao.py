"""Módulo que contém funções para tratar os dados do Webscraping."""

import polars as pl

from modulos.uteis import meu_tempo


def tratar_coluna_string(nome_coluna: str) -> pl.Expr:
    """Tratamento de colunas do tipo string.

    Args:
        nome_coluna (str): Nome da coluna a ser tratada.

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return (
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


def tratar_marca() -> pl.Expr:
    """Tratamento da coluna "marca".

    Preenchimento de valores nulos com "GENERICA".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return tratar_coluna_string("marca").fill_null("GENERICA")


def tratar_produto() -> pl.Expr:
    """Tratamento da coluna "produto".

    Preenchimento de valores nulos com "PRODUTO SEM NOME".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return tratar_coluna_string("produto").fill_null(
        "PRODUTO SEM NOME",
    )


def tratar_preco_velho_reais() -> pl.Expr:
    """Tratamento da coluna "preco_velho_reais".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return pl.col("preco_velho_reais").str.replace(
        ".",
        "",
        literal=True,
    )


def tratar_preco_atual_reais() -> pl.Expr:
    """Tratamento da coluna "preco_atual_reais".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return pl.col("preco_atual_reais").str.replace(
        ".",
        "",
        literal=True,
    )


def tratar_nota_avaliacao() -> pl.Expr:
    """Tratamento da coluna "nota_avaliacao".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return pl.col("nota_avaliacao").fill_null(0).cast(pl.Float32)


def tratar_num_avaliacoes() -> pl.Expr:
    """Tratamento da coluna "num_avaliacoes".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return (
        pl.col("num_avaliacoes")
        .str.strip_chars("()")
        .fill_null(0)
        .cast(pl.Int32)
    )


def tratar_data_coleta() -> pl.Expr:
    """Tratamento da coluna "_data_coleta".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return pl.col("_data_coleta").str.to_datetime(
        format=meu_tempo.formatacao_tempo_completo(),
    )


def tratar_pagina() -> pl.Expr:
    """Tratamento da coluna "_pagina".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return pl.col("_pagina").cast(pl.Int8)


def tratar_ordem() -> pl.Expr:
    """Tratamento da coluna "_ordem".

    Returns:
        pl.Expr: Expressão que trata a coluna.
    """
    return pl.col("_ordem").cast(pl.Int8)


def adiciona_preco_completo(
    col_preco_reais: str,
    col_preco_centavos: str,
    nome_coluna_nova: str,
) -> pl.Expr:
    """Adição de um novo campo com o preço completo.

    Args:
        col_preco_reais (str): Nome da coluna com o preço em reais.
        col_preco_centavos (str): Nome da coluna com o preço em centavos.
        nome_coluna_nova (str): Nome da coluna que será criada.

    Returns:
        pl.Expr: Expressão que adiciona a nova coluna.
    """
    return (
        pl.when(
            pl.col(col_preco_reais).is_not_null()
            & pl.col(col_preco_centavos).is_not_null(),
        )
        .then(pl.col(col_preco_reais) + "." + pl.col(col_preco_centavos))
        .otherwise(
            pl.when(pl.col(col_preco_centavos).is_null())
            .then(pl.col(col_preco_reais))
            .otherwise(None),
        )
        .cast(pl.Float32)
        .alias(nome_coluna_nova)
    )


def adicionar_preco_velho_completo() -> pl.Expr:
    """Adição da coluna "preco_velho".

    Returns:
        pl.Expr: Expressão que adiciona a coluna.
    """
    return adiciona_preco_completo(
        col_preco_reais="preco_velho_reais",
        col_preco_centavos="preco_velho_centavos",
        nome_coluna_nova="preco_velho",
    )


def adicionar_preco_atual_completo() -> pl.Expr:
    """Adição da coluna "preco_atual".

    Returns:
        pl.Expr: Expressão que adiciona a coluna.
    """
    return adiciona_preco_completo(
        col_preco_reais="preco_atual_reais",
        col_preco_centavos="preco_atual_centavos",
        nome_coluna_nova="preco_atual",
    )


def tratar_preco_velho() -> pl.Expr:
    """Tratamento da coluna "preco_velho".

    Returns:
        pl.Expr: Expressão que adiciona a coluna.
    """
    return pl.col("preco_velho").fill_null(pl.col("preco_atual"))


def adicionar_promocao() -> pl.Expr:
    """Adição da coluna "promocao".

    Returns:
        pl.Expr: Expressão que adiciona a coluna.
    """
    return pl.col("preco_velho").is_not_null().alias("promocao")


def adicionar_percentual_promocao() -> pl.Expr:
    """Adição da coluna "percentual_promocao".

    Returns:
        pl.Expr: Expressão que adiciona a coluna.
    """
    return (
        pl.when(pl.col("preco_velho").is_not_null())
        .then(
            100
            * (pl.col("preco_velho") - pl.col("preco_atual"))
            / pl.col("preco_velho"),
        )
        .otherwise(0)
        .alias("percentual_promocao")
    )
