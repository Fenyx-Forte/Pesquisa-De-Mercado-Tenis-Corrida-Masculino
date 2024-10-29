import polars as pl
from etl import extracao, filtros, salvar, transformacao, validar_dados
from loguru import logger
from modulos.uteis import meu_tempo


def tratar_colunas_iniciais(lf: pl.LazyFrame) -> pl.LazyFrame:
    logger.info("Tratando colunas iniciais...")
    return lf.with_columns(
        transformacao.tratar_marca(),
        transformacao.tratar_produto(),
        transformacao.tratar_preco_velho_reais(),
        transformacao.tratar_preco_atual_reais(),
        transformacao.tratar_nota_avaliacao(),
        transformacao.tratar_num_avaliacoes(),
        transformacao.tratar_fonte(),
        transformacao.tratar_site(),
        transformacao.tratar_data_coleta(),
        transformacao.tratar_pagina(),
        transformacao.tratar_ordem(),
    )


def adicionar_precos_completos(lf: pl.LazyFrame) -> pl.LazyFrame:
    logger.info("Adicionando precos completos...")
    return lf.select(
        pl.col("marca"),
        pl.col("produto"),
        transformacao.adicionar_preco_velho_completo(),
        transformacao.adicionar_preco_atual_completo(),
        pl.col("nota_avaliacao"),
        pl.col("num_avaliacoes"),
        pl.col("_fonte"),
        pl.col("_site"),
        pl.col("_data_coleta"),
        pl.col("_pagina"),
        pl.col("_ordem"),
    )


def adicionar_promocao_e_tratar_preco_velho(
    lf: pl.LazyFrame,
) -> pl.LazyFrame:
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
        pl.col("_fonte"),
        pl.col("_site"),
        pl.col("_data_coleta"),
        pl.col("_pagina"),
        pl.col("_ordem"),
    )


def pipeline() -> None:
    logger.info("Inicio pipeline")

    caminho_json = f"../dados/nao_processados/mercado_livre_{meu_tempo.data_agora_simplificada_com_underline()}.json"

    caminho_parquet = f"../dados/processados/mercado_livre_{meu_tempo.data_agora_simplificada_com_underline()}.parquet"

    df = extracao.extrair_dados_json(caminho_json)

    validar_dados.validar_dados_entrada(df)

    lf = df.lazy()

    lf = tratar_colunas_iniciais(lf)

    lf = adicionar_precos_completos(lf)

    lf = adicionar_promocao_e_tratar_preco_velho(lf)

    lf = filtros.remover_valores_null(lf)

    lf = filtros.remover_valores_duplicados(lf)

    df_tratado = lf.collect()

    validar_dados.validar_dados_saida(df_tratado)

    salvar.salvar_dados_parquet(caminho_parquet, df_tratado)

    logger.info("Fim pipeline")
