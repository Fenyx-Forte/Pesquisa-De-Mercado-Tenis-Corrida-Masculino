import math

import pandera.polars as pa
import polars as pl
from etl import transformacao


class MercadoLivreSaida(pa.DataFrameModel):
    marca: pl.String
    produto: pl.String
    preco_velho: pl.Float32 = pa.Field(ge=1)
    preco_atual: pl.Float32 = pa.Field(ge=1)
    promocao: pl.Boolean
    percentual_promocao: pl.Float32 = pa.Field(ge=0, le=100)
    nota_avaliacao: pl.Float32 = pa.Field(ge=0, le=5)
    num_avaliacoes: pl.Int32 = pa.Field(ge=0)

    fonte: pl.String = pa.Field(alias="_fonte")
    site: pl.String = pa.Field(alias="_site")
    data_coleta: pl.Datetime = pa.Field(alias="_data_coleta")
    pagina: pl.Int8 = pa.Field(ge=1, le=10, alias="_pagina")
    ordem: pl.Int8 = pa.Field(ge=1, le=54, alias="_ordem")

    class Config:
        strict = True
        # coerce = True
        # drop_invalid_rows = True

    @pa.check("marca")
    def checa_marca(cls, data: pa.PolarsData) -> pl.LazyFrame:
        return data.lazyframe.select(
            pl.col(data.key) == transformacao.tratar_coluna_string(data.key)
        )

    @pa.check("produto")
    def checa_produto(cls, data: pa.PolarsData) -> pl.LazyFrame:
        return data.lazyframe.select(
            pl.col(data.key) == transformacao.tratar_coluna_string(data.key)
        )

    @pa.check("_fonte")
    def checa_fonte(cls, data: pa.PolarsData) -> pl.LazyFrame:
        return data.lazyframe.select(
            pl.col(data.key)
            == "https://lista.mercadolivre.com.br/tenis-corrida-masculino"
        )

    @pa.check("_site")
    def checa_site(cls, data: pa.PolarsData) -> pl.LazyFrame:
        return data.lazyframe.select(pl.col(data.key) == "MERCADO LIVRE")

    @pa.dataframe_check
    def checa_preco_atual_menor_ou_igual_ao_preco_velho(
        cls, data: pa.PolarsData
    ) -> pl.LazyFrame:
        return data.lazyframe.select(
            pl.col("preco_atual").le(pl.col("preco_velho"))
        )

    @pa.dataframe_check
    def checa_promocao(cls, data: pa.PolarsData) -> pl.LazyFrame:
        return data.lazyframe.select(
            pl.when(pl.col("promocao") is True)
            .then(pl.col("preco_atual") == pl.col("preco_velho"))
            .otherwise(pl.col("preco_atual") <= pl.col("preco_velho"))
        )

    @pa.dataframe_check
    def checa_percentual_promocao(cls, data: pa.PolarsData) -> pl.LazyFrame:
        return data.lazyframe.select(
            abs(
                pl.col("percentual_promocao")
                - (
                    100
                    * (pl.col("preco_velho") - pl.col("preco_atual"))
                    / pl.col("preco_velho")
                )
            )
            <= 0.01
        )

    @pa.dataframe_check
    def checa_nota_avaliacao_precisa_de_ao_menos_uma_avaliacao(
        cls, data: pa.PolarsData
    ) -> pl.LazyFrame:
        return data.lazyframe.select(
            pl.when(pl.col("nota_avaliacao").ge(1))
            .then(pl.col("num_avaliacoes").ge(1))
            .otherwise(pl.lit(True))
        )
