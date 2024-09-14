def query_top_10_marcas_periodo() -> str:
    query = """
    SELECT
        marca AS Marca
        , porcentagem AS Porcentagem
    FROM
        top_10_marcas_periodo('', $data_inicio, $data_fim)
    WHERE
        Marca <> 'GENERICA'
    ORDER BY
        Porcentagem DESC
    LIMIT
        10;
    """

    return query
