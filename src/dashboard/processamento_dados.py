from modulos.uteis import ler_sql, minhas_queries
from polars import DataFrame


def dados_mais_recentes() -> DataFrame:
    query = minhas_queries.dados_mais_recentes_do_banco_de_dados()

    return ler_sql.query_banco_de_dados_apenas_leitura(query)


def data_coleta(df: DataFrame) -> str:
    query_data_coleta = minhas_queries.data_coleta_mais_recente()
    df_data_coleta = ler_sql.query_pl_para_pl(query_data_coleta, df)

    data_coleta = df_data_coleta.item(0, 0)
    horario_coleta = df_data_coleta.item(0, 1)

    return f"{data_coleta} - {horario_coleta}"


def inicializacao_pagina_2(df: DataFrame) -> list[dict]:
    return df.select(
        "marca", "preco_atual", "promocao", "percentual_promocao"
    ).to_dicts()
