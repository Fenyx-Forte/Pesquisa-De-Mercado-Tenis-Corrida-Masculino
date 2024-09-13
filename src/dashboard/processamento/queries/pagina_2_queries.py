def query_top_10_marcas_atuais() -> str:
    query = """
    WITH marcas_agrupadas AS (
        SELECT
            dmr.marca AS marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) AS porcentagem
        FROM
            dados_mais_recentes AS dmr
        GROUP BY
            dmr.marca
    )
    SELECT
        marca AS Marca
        , porcentagem AS Porcentagem
        , $periodo AS Periodo
    FROM
        marcas_agrupadas
    WHERE
        Marca <> 'GENERICA'
    ORDER BY
        porcentagem DESC
    LIMIT
        10;
    """

    return query


def query_top_10_marcas_periodo() -> str:
    query = """
    WITH tabela_reserva AS (
        SELECT
            unnest($lista_marcas) AS marca,
            0.0 AS porcentagem,
            $periodo AS periodo
    ),
    tabela_principal AS (
        SELECT
            marca
            , porcentagem
            , periodo
        FROM
            top_10_marcas_periodo($periodo, $data_inicio, $data_fim)
        WHERE
            marca IN (SELECT UNNEST ($lista_marcas))
        ORDER BY
            porcentagem DESC
    )
    SELECT
        COALESCE(t1.marca, t2.marca) AS Marca
        , COALESCE(t1.porcentagem, t2.porcentagem) AS Porcentagem
        , COALESCE(t1.periodo, t2.periodo) AS Periodo
    FROM
        tabela_principal AS t1
    RIGHT JOIN
        tabela_reserva AS t2
        ON t1.marca = t2.marca
    ORDER BY
        Porcentagem DESC
    LIMIT
        10;
    """

    return query
