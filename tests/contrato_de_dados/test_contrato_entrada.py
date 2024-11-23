import os
import sys

# Adiciona a pasta 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join("./", "src")))

import pandera.polars as pa
import polars as pl
import pytest

from src.modulos.contrato_de_dados import contrato_entrada
from src.modulos.uteis import meu_tempo


def test_contrato_correto():
    data = meu_tempo.data_agora_string()

    df = pl.DataFrame(
        {
            "marca": ["A", None, "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho_reais": ["100", None, "200"],
            "preco_velho_centavos": ["50", "40", None],
            "preco_atual_reais": ["80", "200", "150"],
            "preco_atual_centavos": ["0", "0", None],
            "nota_avaliacao": [None, "3", "4"],
            "num_avaliacoes": [None, "5", "4"],
            "_data_coleta": [data, data, data],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        }
    )

    contrato_entrada.TenisCorridaEntrada.validate(df)


def test_produto_null():
    data = meu_tempo.data_agora_string()

    df = pl.DataFrame(
        {
            "marca": ["A", None, "C"],
            "produto": ["TENIS A", None, "TENIS C"],
            "preco_velho_reais": ["100", None, "200"],
            "preco_velho_centavos": ["50", "40", None],
            "preco_atual_reais": ["80", "200", "150"],
            "preco_atual_centavos": ["0", "0", None],
            "nota_avaliacao": [None, "3", "4"],
            "num_avaliacoes": [None, "5", "4"],
            "_data_coleta": [data, data, data],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        }
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_entrada.TenisCorridaEntrada.validate(df)


def test_data_coleta_null():
    data = meu_tempo.data_agora_string()

    df = pl.DataFrame(
        {
            "marca": ["A", None, "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho_reais": ["100", None, "200"],
            "preco_velho_centavos": ["50", "40", None],
            "preco_atual_reais": ["80", "200", "150"],
            "preco_atual_centavos": ["0", "0", None],
            "nota_avaliacao": [None, "3", "4"],
            "num_avaliacoes": [None, "5", "4"],
            "_data_coleta": [None, data, data],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        }
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_entrada.TenisCorridaEntrada.validate(df)


def test_pagina_null():
    data = meu_tempo.data_agora_string()

    df = pl.DataFrame(
        {
            "marca": ["A", None, "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho_reais": ["100", None, "200"],
            "preco_velho_centavos": ["50", "40", None],
            "preco_atual_reais": ["80", "200", "150"],
            "preco_atual_centavos": ["0", "0", None],
            "nota_avaliacao": [None, "3", "4"],
            "num_avaliacoes": [None, "5", "4"],
            "_data_coleta": [data, data, data],
            "_pagina": [None, 1, 1],
            "_ordem": [1, 2, 3],
        }
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_entrada.TenisCorridaEntrada.validate(df)


def test_pagina_incorreta():
    data = meu_tempo.data_agora_string()

    df = pl.DataFrame(
        {
            "marca": ["A", None, "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho_reais": ["100", None, "200"],
            "preco_velho_centavos": ["50", "40", None],
            "preco_atual_reais": ["80", "200", "150"],
            "preco_atual_centavos": ["0", "0", None],
            "nota_avaliacao": [None, "3", "4"],
            "num_avaliacoes": [None, "5", "4"],
            "_data_coleta": [data, data, data],
            "_pagina": [-1, 111, 1],
            "_ordem": [1, 2, 3],
        }
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_entrada.TenisCorridaEntrada.validate(df)


def test_ordem_null():
    data = meu_tempo.data_agora_string()

    df = pl.DataFrame(
        {
            "marca": ["A", None, "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho_reais": ["100", None, "200"],
            "preco_velho_centavos": ["50", "40", None],
            "preco_atual_reais": ["80", "200", "150"],
            "preco_atual_centavos": ["0", "0", None],
            "nota_avaliacao": [None, "3", "4"],
            "num_avaliacoes": [None, "5", "4"],
            "_data_coleta": [data, data, data],
            "_pagina": [1, 1, 1],
            "_ordem": [None, 2, 3],
        }
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_entrada.TenisCorridaEntrada.validate(df)


def test_ordem_incorreta():
    data = meu_tempo.data_agora_string()

    df = pl.DataFrame(
        {
            "marca": ["A", None, "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho_reais": ["100", None, "200"],
            "preco_velho_centavos": ["50", "40", None],
            "preco_atual_reais": ["80", "200", "150"],
            "preco_atual_centavos": ["0", "0", None],
            "nota_avaliacao": [None, "3", "4"],
            "num_avaliacoes": [None, "5", "4"],
            "_data_coleta": [data, data, data],
            "_pagina": [1, 1, 1],
            "_ordem": [-1, 74, 3],
        }
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_entrada.TenisCorridaEntrada.validate(df)
