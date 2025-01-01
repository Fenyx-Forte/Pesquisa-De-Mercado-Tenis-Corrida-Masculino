"""Contrato de dados para os dados de saída do ETL."""

import pandera.polars as pa
import polars as pl

from etl.legado_polars import transformacao


class TenisCorridaSaida(pa.DataFrameModel):
    """Contrato de dados para os dados de saída do ETL referentes a tênis de corrida."""

    marca: pl.String
    produto: pl.String
    preco_velho: pl.Float32 = pa.Field(ge=1)
    preco_atual: pl.Float32 = pa.Field(ge=1)
    promocao: pl.Boolean
    percentual_promocao: pl.Float32 = pa.Field(ge=0, le=100)
    nota_avaliacao: pl.Float32 = pa.Field(ge=0, le=5)
    num_avaliacoes: pl.Int32 = pa.Field(ge=0)

    data_coleta: pl.Date = pa.Field(alias="_data_coleta")
    horario_coleta: pl.Time = pa.Field(alias="_horario_coleta")
    pagina: pl.Int8 = pa.Field(ge=1, le=10, alias="_pagina")
    ordem: pl.Int8 = pa.Field(ge=1, le=72, alias="_ordem")

    class Config:
        """Configuração do contrato de dados."""

        strict = True

    @pa.check("marca")
    def checa_marca(self, data: pa.PolarsData) -> pl.LazyFrame:
        """Verifica se a coluna "marca" foi tratada corretamente.

        Args:
            data (pa.PolarsData): Dados do dataframe.

        Returns:
            pl.LazyFrame: Dados verificados.
        """
        return data.lazyframe.select(
            pl.col(data.key) == transformacao.tratar_coluna_string(data.key),
        )

    @pa.check("produto")
    def checa_produto(self, data: pa.PolarsData) -> pl.LazyFrame:
        """Verifica se a coluna "produto" foi tratada corretamente.

        Args:
            data (pa.PolarsData): Dados do dataframe.

        Returns:
            pl.LazyFrame: Dados verificados.
        """
        return data.lazyframe.select(
            pl.col(data.key) == transformacao.tratar_coluna_string(data.key),
        )

    @pa.dataframe_check
    def checa_preco_atual_menor_ou_igual_ao_preco_velho(
        self,
        data: pa.PolarsData,
    ) -> pl.LazyFrame:
        """Verifica se a coluna "preco_atual" é menor ou igual à coluna "preco_velho".

        Args:
            data (pa.PolarsData): Dados do dataframe.

        Returns:
            pl.LazyFrame: Dados verificados.
        """
        return data.lazyframe.select(
            pl.col("preco_atual").le(pl.col("preco_velho")),
        )

    @pa.dataframe_check
    def checa_promocao(self, data: pa.PolarsData) -> pl.LazyFrame:
        """Verifica se a coluna "promocao" está correta.

        Para isso, verifica se a coluna "promocao" é True quando realmente houver uma promoção, ou se é False quando não houver promoção.

        Args:
            data (pa.PolarsData): Dados do dataframe.

        Returns:
            pl.LazyFrame: Dados verificados.
        """
        return data.lazyframe.select(
            pl.when(pl.col("promocao") is True)
            .then(pl.col("preco_atual") == pl.col("preco_velho"))
            .otherwise(pl.col("preco_atual") <= pl.col("preco_velho")),
        )

    @pa.dataframe_check
    def checa_percentual_promocao(self, data: pa.PolarsData) -> pl.LazyFrame:
        """Verifica se a coluna "percentual_promocao" está correta.

        Para isso, verifica se a coluna "percentual_promocao" é aproximadamente igual ao percentual promoção calculado através dos preços.

        Args:
            data (pa.PolarsData): Dados do dataframe.

        Returns:
            pl.LazyFrame: Dados verificados.
        """
        return data.lazyframe.select(
            abs(
                pl.col("percentual_promocao")
                - (
                    100
                    * (pl.col("preco_velho") - pl.col("preco_atual"))
                    / pl.col("preco_velho")
                ),
            )
            <= 0.01,
        )

    @pa.dataframe_check
    def checa_nota_avaliacao_precisa_de_ao_menos_uma_avaliacao(
        self,
        data: pa.PolarsData,
    ) -> pl.LazyFrame:
        """Verifica se produtos com nota de avaliação maior ou igual a 1 tem pelo menos 1 avaliação.

        Args:
            data (pa.PolarsData): Dados do dataframe.

        Returns:
            pl.LazyFrame: Dados verificados.
        """
        return data.lazyframe.select(
            pl.when(pl.col("nota_avaliacao").ge(1))
            .then(pl.col("num_avaliacoes").ge(1))
            .otherwise(pl.lit(value=True)),
        )
