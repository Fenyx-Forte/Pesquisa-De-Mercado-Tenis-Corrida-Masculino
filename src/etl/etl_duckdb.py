from etl import (
    duckdb_local,
    extracao_sql,
    salvar_sql,
    validar_dados,
)
from loguru import logger
from modulos.uteis import ler_sql, meu_tempo, minhas_queries


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
    query_entrada = minhas_queries.cast_polars_entrada()

    validar_dados.validar_dados_entrada(
        ler_sql.query_duckbdb_para_pl(query_entrada, df)
    )

    # Transformacao
    caminho_query = "../sql/transformacao/tratamento_mercado_livre.sql"

    query_transfomacao = ler_sql.ler_conteudo_query(caminho_query)

    df = ler_sql.query_duckdb_para_duckdb(query_transfomacao, df)

    # Validacao
    query_saida = minhas_queries.cast_polars_saida()

    validar_dados.validar_dados_saida(
        ler_sql.query_duckbdb_para_pl(query_saida, df)
    )

    # Salvar
    query_insercao = ler_sql.ler_conteudo_query("../sql/dml/inserir_dados.sql")

    salvar_sql.salvar_dados(df, query_insercao, nome_arquivo, horario)
