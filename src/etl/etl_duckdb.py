import duckdb
import polars as pl
from etl import validar_dados
from loguru import logger
from modulos.uteis import ler_sql, meu_tempo


def extracao_dados(caminho_json: str) -> duckdb.DuckDBPyRelation:
    logger.info("Extraindo dados...")

    df = duckdb.read_json(caminho_json)

    logger.info("Dados extraidos")

    return df


def transformacao(
    query: str, df: duckdb.DuckDBPyRelation
) -> duckdb.DuckDBPyRelation:
    logger.info("Realizando transformacoes...")

    df = duckdb.sql(query)

    logger.info("Transformacoes realizadas")

    return df


def salvar_dados(df: duckdb.DuckDBPyRelation, caminho_parquet: str) -> None:
    logger.info("Salvando dados...")

    df.write_parquet(caminho_parquet)

    logger.info("Dados salvos")


def pipeline() -> None:
    logger.info("Inicio pipeline")

    caminho_json = f"../dados/nao_processados/mercado_livre_{meu_tempo.data_agora_simplificada_com_underline()}.json"

    caminho_parquet = f"../dados/processados/mercado_livre_{meu_tempo.data_agora_simplificada_com_underline()}.parquet"

    caminho_query = "../sql/queries/tratamento_mercado_livre.sql"

    df = extracao_dados(caminho_json)

    cast_dict_entrada = {
        "_data_coleta": pl.String,
    }

    validar_dados.validar_dados_entrada(df.pl().cast(cast_dict_entrada))

    query = ler_sql.ler_conteudo_query(caminho_query)

    df = transformacao(query, df)

    df.show()

    validar_dados.validar_dados_saida(
        df.pl().with_columns(
            pl.col("preco_velho").cast(pl.Float32),
            pl.col("preco_atual").cast(pl.Float32),
            pl.col("percentual_promocao").cast(pl.Float32),
            pl.col("nota_avaliacao").cast(pl.Float32),
            pl.col("num_avaliacoes").cast(pl.Int32),
            pl.col("_pagina").cast(pl.Int8),
            pl.col("_ordem").cast(pl.Int8),
        )
    )

    salvar_dados(df, caminho_parquet)

    logger.info("Fim pipeline")
