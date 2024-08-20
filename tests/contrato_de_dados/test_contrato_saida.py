import os
import sys

# Adiciona a pasta 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join("./", "src")))

from datetime import datetime

import pandera.polars as pa
import polars as pl
import pytest

from src.modulos.contrato_de_dados import contrato_saida


def test_contrato_correto():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    contrato_saida.MercadoLivreSaida.validate(df)


def test_marca_com_caracteres_especiais():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["Ã", "B ", "C  D"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_produto_com_caracteres_especiais():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TÊNIS B", "TENIS  C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_preco_velho_fora_intervalo():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [-100.0, 0.99, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [False, False, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_preco_velho_menor_do_que_preco_atual():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [50.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [False, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_preco_atual_fora_intervalo():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 160.0, -100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_percentual_promocao_fora_intervalo():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [-30.0, 140.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_nota_avaliacao_fora_intervalo():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [-3.5, 2.5, 15.0],
            "num_avaliacoes": [3, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_nota_avaliacao_sem_avaliacao():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [4.5, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_num_avaliacoes_fora_intervalo():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [3.0, 2.5, 5.0],
            "num_avaliacoes": [-10, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_pagina_fora_intervalo():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [-1, 11, 0],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_ordem_fora_intervalo():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [-1, 0, 55],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_fonte_incorreta():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculin",
            ],
            "_site": ["MERCADO LIVRE", "MERCADO LIVRE", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)


def test_site_incorreto():
    data_completa = datetime.now()
    data = data_completa.date()
    horario = data_completa.time()

    df = pl.DataFrame(
        {
            "marca": ["A", "B", "C"],
            "produto": ["TENIS A", "TENIS B", "TENIS C"],
            "preco_velho": [100.0, 100.0, 100.0],
            "preco_atual": [70.0, 60.0, 100.0],
            "promocao": [True, True, False],
            "percentual_promocao": [30.0, 40.0, 0.0],
            "nota_avaliacao": [0, 2.5, 5.0],
            "num_avaliacoes": [0, 4, 1000],
            "_fonte": [
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
                "https://lista.mercadolivre.com.br/tenis-corrida-masculino",
            ],
            "_site": ["MERCADO LIV", "MERCADO", "MERCADO LIVRE"],
            "_data_coleta": [data, data, data],
            "_horario_coleta": [horario, horario, horario],
            "_pagina": [1, 1, 1],
            "_ordem": [1, 2, 3],
        },
        schema_overrides={
            "preco_velho": pl.Float32,
            "preco_atual": pl.Float32,
            "percentual_promocao": pl.Float32,
            "nota_avaliacao": pl.Float32,
            "num_avaliacoes": pl.Int32,
            "_pagina": pl.Int8,
            "_ordem": pl.Int8,
        },
    )

    with pytest.raises(pa.errors.SchemaError):
        contrato_saida.MercadoLivreSaida.validate(df)
