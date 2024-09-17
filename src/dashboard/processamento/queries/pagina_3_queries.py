def query_top_10_marcas_periodo() -> str:
    query = """
    SELECT
        t.marca AS Marca
        , t.porcentagem AS Porcentagem
    FROM
        top_10_marcas_periodo('', $data_inicio, $data_fim) AS t
    WHERE
        t.marca <> 'GENERICA'
    ORDER BY
        t.porcentagem DESC
    LIMIT
        10;
    """

    return query
