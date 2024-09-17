def query_satisfacao_hoje() -> str:
    query = """
    WITH tabela_resultado AS (
        SELECT
            dmr.marca
            , AVG(dmr.nota_avaliacao) AS nota_avaliacao
            , AVG(dmr.num_avaliacoes) AS num_avaliacoes
        FROM
            dados_mais_recentes AS dmr
        WHERE
            dmr.num_avaliacoes > 0
        GROUP BY
            dmr.marca
    )

    SELECT
        tr.marca
        , tr.nota_avaliacao
        , tr.num_avaliacoes
        , 'num_avaliacoes' AS tipo_linha
    FROM
        tabela_resultado AS tr
    WHERE
        tr.num_avaliacoes > 20

    UNION ALL

    SELECT
        tr.marca
        , tr.nota_avaliacao
        , tr.num_avaliacoes
        , 'avaliacao' AS tipo_linha
    FROM
        tabela_resultado AS tr
    WHERE
        tr.nota_avaliacao > 4;
    """

    return query


def query_satisfacao_periodo() -> str:
    query = """
    WITH tabela_resultado AS (
        SELECT
            map.marca
            , map.nota_avaliacao
            , map.num_avaliacoes
        FROM
            media_avaliacoes_periodo($data_inicio, $data_fim) AS map
    )
    SELECT
        tr.marca
        , tr.nota_avaliacao
        , tr.num_avaliacoes
        , 'num_avaliacoes' AS tipo_linha
    FROM
        tabela_resultado AS tr
    WHERE
        tr.num_avaliacoes > 20

    UNION ALL

    SELECT
        tr.marca
        , tr.nota_avaliacao
        , tr.num_avaliacoes
        , 'avaliacao' AS tipo_linha
    FROM
        tabela_resultado AS tr
    WHERE
        tr.nota_avaliacao > 4;
    """

    return query
