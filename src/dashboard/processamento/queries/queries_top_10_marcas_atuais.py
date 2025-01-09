"""Queries usadas na página Top 10 Marcas Atuais."""


def query_top_10_marcas_periodo() -> str:
    """Query para calcular os dados de um determinado período.

    Returns:
        str: Query com os dados de um determinado período.
    """
    return """
    WITH tabela_reserva AS (
        SELECT
            unnest($lista_marcas) AS marca,
            0.0 AS porcentagem,
            $periodo AS periodo
    ),
    tabela_principal AS (
        SELECT
            t.marca
            , t.porcentagem
            , t.periodo
        FROM
            top_10_marcas_periodo($periodo, $data_inicio, $data_fim) AS t
        WHERE
            t.marca IN (SELECT UNNEST ($lista_marcas))
        ORDER BY
            t.porcentagem DESC
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
