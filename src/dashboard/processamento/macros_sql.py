def top_10_marcas_atuais() -> str:
    query = """
    CREATE OR REPLACE MACRO top_10_marcas_atuais(periodo) AS TABLE
        SELECT
            dmr.marca as Marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) as Porcentagem
            , periodo as Período
        FROM
            dados_mais_recentes as dmr
        GROUP BY
            dmr.marca;
    """

    return query


def top_10_marcas_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO top_10_marcas_periodo(periodo, data_inicio, data_fim) AS TABLE
        SELECT
            dc.marca as Marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) as Porcentagem
            , periodo as Período
        FROM
            dados_completos as dc
        WHERE
            dc.data_coleta BETWEEN data_inicio AND data_fim
        GROUP BY
            dc.marca;
    """

    return query
