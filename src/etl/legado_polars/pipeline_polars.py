"""Módulo da pipeline ETL para os dados do webscraping.

A pipeline foi feita utilizando o Polars.
"""

import polars as pl
from loguru import logger

from etl import validar_dados
from etl.legado_polars import (
    extracao,
    filtros,
    salvar,
    transformacao,
)
from modulos.uteis import meu_tempo


def tratar_colunas_iniciais(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Trata as colunas dos dados do webscraping.

    Esse é o 1o passo da pipeline.

    Args:
        lf (pl.LazyFrame): Dados iniciais do webscraping.

    Returns:
        pl.LazyFrame: Dados após o 1o tratamento.
    """
    logger.info("Tratando colunas iniciais...")
    return lf.with_columns(
        transformacao.tratar_marca(),
        transformacao.tratar_produto(),
        transformacao.tratar_preco_velho_reais(),
        transformacao.tratar_preco_atual_reais(),
        transformacao.tratar_nota_avaliacao(),
        transformacao.tratar_num_avaliacoes(),
        transformacao.tratar_data_coleta(),
        transformacao.tratar_pagina(),
        transformacao.tratar_ordem(),
    )


def adicionar_precos_completos(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Adiciona 2 novas colunas: preco_velho_completo e preco_atual_completo.

    Esse é o 2o passo da pipeline.

    Args:
        lf (pl.LazyFrame): Dados após o 1o tratamento.

    Returns:
        pl.LazyFrame: Dados após o 2o tratamento.
    """
    logger.info("Adicionando precos completos...")
    return lf.select(
        pl.col("marca"),
        pl.col("produto"),
        transformacao.adicionar_preco_velho_completo(),
        transformacao.adicionar_preco_atual_completo(),
        pl.col("nota_avaliacao"),
        pl.col("num_avaliacoes"),
        pl.col("_data_coleta"),
        pl.col("_pagina"),
        pl.col("_ordem"),
    )


def adicionar_promocao_e_tratar_preco_velho(
    lf: pl.LazyFrame,
) -> pl.LazyFrame:
    """Adiciona as colunas 'promocao' e 'percentual_promocao' e trata a coluna 'preco_velho'.

    Esse é o 3o passo da pipeline.

    Args:
        lf (pl.LazyFrame): Dados após o 2o tratamento.

    Returns:
        pl.LazyFrame: Dados após o 3o tratamento.
    """
    logger.info("Adicionando colunas de promocao e tratando preco_velho...")
    return lf.select(
        pl.col("marca"),
        pl.col("produto"),
        transformacao.tratar_preco_velho(),
        pl.col("preco_atual"),
        transformacao.adicionar_promocao(),
        transformacao.adicionar_percentual_promocao(),
        pl.col("nota_avaliacao"),
        pl.col("num_avaliacoes"),
        pl.col("_data_coleta"),
        pl.col("_pagina"),
        pl.col("_ordem"),
    )


def pipeline() -> None:
    """Pipeline ETL para os dados do webscraping.

    O tratamento dos dados tem 5 etapas:
    1. Tratar as colunas iniciais.
    2. Adicionar as colunas 'preco_velho_completo' e 'preco_atual_completo'.
    3. Adicionar as colunas 'promocao' e 'percentual_promocao' e tratar a coluna 'preco_velho'.
    4. Remover valores nulos.
    5. Remover valores duplicados.
    """
    logger.info("Inicio pipeline")

    caminho_json = f"../dados/nao_processados/tenis_corrida_{meu_tempo.data_agora_simplificada_com_underline()}.json"

    caminho_parquet = f"../dados/processados/tenis_corrida_{meu_tempo.data_agora_simplificada_com_underline()}.parquet"

    df_entrada = extracao.extrair_dados_json(caminho_json)

    validar_dados.validar_dados_entrada(df_entrada)

    lf = df_entrada.lazy()

    lf = tratar_colunas_iniciais(lf)

    lf = adicionar_precos_completos(lf)

    lf = adicionar_promocao_e_tratar_preco_velho(lf)

    lf = filtros.remover_valores_null(lf)

    lf = filtros.remover_valores_duplicados(lf)

    df_tratado = lf.collect()

    validar_dados.validar_dados_saida(df_tratado)

    salvar.salvar_dados_parquet(caminho_parquet, df_tratado)

    logger.info("Fim pipeline")
