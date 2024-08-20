import polars as pl
from etl import (
    duckdb_local,
    extracao_sql,
    salvar_sql,
    validar_dados,
)
from loguru import logger
from modulos.uteis import ler_sql, meu_tempo


def pipeline() -> None:
    # Extracao
    horario = meu_tempo.data_agora_string()

    nome_arquivo = (
        f"mercado_livre_{meu_tempo.data_agora_simplificada_com_underline()}"
    )

    caminho_json = f"../dados/nao_processados/{nome_arquivo}.json"

    # Verificacao
    arquivo_ja_foi_salvo = duckdb_local.verifica_se_arquivo_ja_foi_salvo(
        nome_arquivo
    )

    if arquivo_ja_foi_salvo:
        logger.info("Arquivo ja foi salvo no banco de dados!")
        return None

    df = extracao_sql.extracao_json(caminho_json)

    # Validacao
    cast_dict_entrada = {
        "_data_coleta": pl.String,
    }

    validar_dados.validar_dados_entrada(df.pl().cast(cast_dict_entrada))

    # Transformacao
    caminho_query = "../sql/transformacao/tratamento_mercado_livre.sql"

    df = ler_sql.query_df(caminho_query, df)

    # Validacao
    cast_dict_saida = {
        "preco_velho": pl.Float32,
        "preco_atual": pl.Float32,
        "percentual_promocao": pl.Float32,
        "nota_avaliacao": pl.Float32,
        "num_avaliacoes": pl.Int32,
        "_pagina": pl.Int8,
        "_ordem": pl.Int8,
    }

    validar_dados.validar_dados_saida(df.pl().cast(cast_dict_saida))

    # Salvar
    query_insercao = ler_sql.ler_conteudo_query("../sql/dml/inserir_dados.sql")

    salvar_sql.salvar_dados(df, query_insercao, nome_arquivo, horario)
