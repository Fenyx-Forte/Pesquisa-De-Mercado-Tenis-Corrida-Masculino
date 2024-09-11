def top_10_marcas_atuais() -> str:
    query = """
    CREATE OR REPLACE MACRO top_10_marcas_atuais(periodo) AS TABLE
        SELECT
            dmr.marca AS marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) AS porcentagem
            , periodo AS periodo
        FROM
            dados_mais_recentes AS dmr
        GROUP BY
            dmr.marca;
    """

    return query


def top_10_marcas_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO top_10_marcas_periodo(periodo, data_inicio, data_fim) AS TABLE
        SELECT
            dc.marca AS marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) AS porcentagem
            , periodo AS periodo
        FROM
            dados_completos AS dc
        WHERE
            dc.data_coleta BETWEEN data_inicio AND data_fim
        GROUP BY
            dc.marca;
    """

    return query


def top_10_marcas_historico() -> str:
    query = """
    CREATE OR REPLACE MACRO top_10_marcas_historico(periodo) AS TABLE
        SELECT
            dc.marca AS marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) AS porcentagem
            , periodo AS periodo
        FROM
            dados_completos AS dc
        GROUP BY
            dc.marca;
    """

    return query
