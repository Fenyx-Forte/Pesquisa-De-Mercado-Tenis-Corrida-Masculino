def query_satisfacao_hoje() -> str:
    query = """
    WITH tabela_resultado AS (
        SELECT
            marca
            , AVG(avaliacao) AS avaliacao
            , AVG(num_avaliacoes) AS num_avaliacoes
        FROM
            dados_mais_recentes
    )

    SELECT
        marca
        , avaliacao
        , num_avaliacoes
        , 'num_avaliacoes' AS tipo_linha
    FROM
        tabela_resultado
    WHERE
        num_avaliacoes > 20

    UNION ALL

    SELECT
        marca
        , avaliacao
        , num_avaliacoes
        , 'avaliacao' AS tipo_linha
    FROM
        tabela_resultado
    WHERE
        avaliacao > 4;
    """

    return query


def query_satisfacao_periodo() -> str:
    query = """
    WITH tabela_resultado AS (
        SELECT
            marca
            , avaliacao
            , num_avaliacoes
        FROM
            media_avaliacoes_periodo($data_inicio, $data_fim)
    )
    SELECT
        marca
        , avaliacao
        , num_avaliacoes
        , 'num_avaliacoes' AS tipo_linha
    FROM
        tabela_resultado
    WHERE
        num_avaliacoes > 20

    UNION ALL

    SELECT
        marca
        , avaliacao
        , num_avaliacoes
        , 'avaliacao' AS tipo_linha
    FROM
        tabela_resultado
    WHERE
        avaliacao > 4;
    """

    return query
