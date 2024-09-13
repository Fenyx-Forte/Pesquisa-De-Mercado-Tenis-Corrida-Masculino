def query_top_10_marcas_atuais() -> str:
    query = """
    SELECT
        marca AS Marca
        , porcentagem AS Porcentagem
        , periodo AS Periodo
    FROM
        top_10_marcas_atuais($periodo)
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
    WITH tabela_reservas AS (
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
        tabela_reservas AS t2
        ON t1.marca = t2.marca
    ORDER BY
        Porcentagem DESC
    LIMIT
        10;
    """

    return query
