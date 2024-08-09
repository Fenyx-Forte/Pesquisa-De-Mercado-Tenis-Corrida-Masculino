from functools import partial

import pandera.polars as pa
import polars as pl

campo_string_padrao = partial(pa.Field, nullable=True)


class MercadoLivreEntrada(pa.DataFrameModel):
    marca: pl.String = campo_string_padrao()
    produto: pl.String = campo_string_padrao()
    preco_velho_reais: pl.String = campo_string_padrao()
    preco_velho_centavos: pl.String = campo_string_padrao()
    preco_atual_reais: pl.String = campo_string_padrao()
    preco_atual_centavos: pl.String = campo_string_padrao()
    nota_avaliacao: pl.String = campo_string_padrao()
    num_avaliacoes: pl.String = campo_string_padrao()
    fonte: pl.String = pa.Field(alias="_fonte")
    site: pl.String = pa.Field(alias="_site")
    data_coleta: pl.String = pa.Field(alias="_data_coleta")
    pagina: pl.Int64 = pa.Field(alias="_pagina")
    ordem: pl.Int64 = pa.Field(alias="_ordem")

    class Config:
        strict = True
        # coerce = True
        # drop_invalid_rows = True
