import duckdb
import pandera.polars as pa
import polars as pl
from loguru import logger
from modulos.contrato_de_dados import contrato_entrada, contrato_saida
from modulos.transformacao import mercado_livre


def extrair_dados_json(caminho_arquivo: str) -> pl.DataFrame:
    logger.info("Extraindo dados json...")
    return pl.read_json(caminho_arquivo)


def validar_dados_entrada(df: pl.DataFrame) -> None:
    logger.info("Validando dados de entrada...")
    try:
        contrato_entrada.MercadoLivreEntrada.validate(df)
        logger.info("Dados validos")
    except pa.errors.SchemaError as exc:
        logger.error(exc)


def validar_dados_saida(df: pl.DataFrame) -> None:
    logger.info("Validando dados de saida...")
    try:
        contrato_saida.MercadoLivreSaida.validate(df)
        logger.info("Dados validos")
    except pa.errors.SchemaError as exc:
        logger.error(exc)


def tratando_colunas_iniciais(lf: pl.LazyFrame) -> pl.LazyFrame:
    logger.info("Tratando colunas iniciais...")
    return lf.with_columns(
        mercado_livre.tratar_marca(),
        mercado_livre.tratar_produto(),
        mercado_livre.tratar_preco_velho_reais(),
        mercado_livre.tratar_preco_atual_reais(),
        mercado_livre.tratar_nota_avaliacao(),
        mercado_livre.tratar_num_avaliacoes(),
        mercado_livre.tratar_fonte(),
        mercado_livre.tratar_site(),
        mercado_livre.tratar_data_coleta(),
        mercado_livre.tratar_pagina(),
        mercado_livre.tratar_ordem(),
    )


def adicionando_precos_completos(lf: pl.LazyFrame) -> pl.LazyFrame:
    logger.info("Adicionando precos completos...")
    return lf.select(
        pl.col("marca"),
        pl.col("produto"),
        mercado_livre.adicionar_preco_velho_completo(),
        mercado_livre.adicionar_preco_atual_completo(),
        pl.col("nota_avaliacao"),
        pl.col("num_avaliacoes"),
        pl.col("_fonte"),
        pl.col("_site"),
        pl.col("_data_coleta"),
        pl.col("_pagina"),
        pl.col("_ordem"),
    )


def adicionando_promocao_e_tratando_preco_velho(
    lf: pl.LazyFrame,
) -> pl.LazyFrame:
    logger.info("Adicionando colunas de promocao e tratando preco_velho...")
    return lf.select(
        pl.col("marca"),
        pl.col("produto"),
        mercado_livre.tratar_preco_velho(),
        pl.col("preco_atual"),
        mercado_livre.adicionar_promocao(),
        mercado_livre.adicionar_percentual_promocao(),
        pl.col("nota_avaliacao"),
        pl.col("num_avaliacoes"),
        pl.col("_fonte"),
        pl.col("_site"),
        pl.col("_data_coleta"),
        pl.col("_pagina"),
        pl.col("_ordem"),
    )


def removendo_valores_null(lf: pl.LazyFrame) -> pl.LazyFrame:
    logger.info("Removendo valores null da coluna 'preco_atual'")
    return lf.drop_nulls("preco_atual")


def removendo_valores_duplicados(lf: pl.LazyFrame) -> pl.LazyFrame:
    logger.info("Removendo linhas duplicadas")
    return lf.unique()


def salvar_dados_parquet(caminho_arquivo: str, df: pl.DataFrame) -> None:
    logger.info("Salvando dados em parquet...")
    df.write_parquet(caminho_arquivo)
    logger.info("Dados salvos!")


def pipeline(caminho_json: str, caminho_parquet: str) -> None:
    logger.info("Inicio Pipeline")

    df = extrair_dados_json(caminho_json)

    validar_dados_entrada(df)

    lf = df.lazy()

    lf = tratando_colunas_iniciais(lf)

    lf = adicionando_precos_completos(lf)

    lf = adicionando_promocao_e_tratando_preco_velho(lf)

    lf = removendo_valores_null(lf)

    lf = removendo_valores_duplicados(lf)

    df_tratado = lf.collect()

    validar_dados_saida(df_tratado)

    salvar_dados_parquet(caminho_parquet, df_tratado)

    logger.info("Fim pipeline!")
