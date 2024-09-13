def query_top_10_marcas_historico() -> str:
    query = """
    SELECT
        marca AS Marca
        , porcentagem AS Porcentagem
        , periodo AS Periodo
    FROM
        top_10_marcas_periodo($periodo, $data_inicio, $data_fim)
    WHERE
        Marca <> 'GENERICA'
    ORDER BY
        Porcentagem DESC
    LIMIT
        10;
    """

    return query


def query_top_10_marcas_periodo() -> str:
    query = """
    SELECT
        marca AS Marca
        , porcentagem AS Porcentagem
        , periodo AS Periodo
    FROM
        top_10_marcas_periodo($periodo, $data_inicio, $data_fim)
    WHERE
        Marca <> 'GENERICA'
    ORDER BY
        Porcentagem DESC
    LIMIT
        10;
    """

    return query
