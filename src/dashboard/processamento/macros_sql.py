def macro_dados_completos_por_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO dados_completos_por_periodo(data_inicio, data_fim) AS TABLE
        SELECT
            marca
            , preco_atual
            , promocao
            , percentual_promocao
            , nota_avaliacao
            , num_avaliacoes
            , data_coleta
        FROM
            dados_completos
        WHERE
            data_coleta BETWEEN data_inicio AND data_fim;
    """

    return query


def macro_top_10_marcas_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO top_10_marcas_periodo(periodo, data_inicio, data_fim) AS TABLE
        WITH porcentagem_por_dia AS (
            SELECT
                marca AS marca
                , (
                    COUNT(*) * 100.0 / (SUM(COUNT(*)) OVER(PARTITION BY data_coleta))
                ) AS porcentagem
            FROM
                dados_completos_por_periodo(data_inicio, data_fim)
            GROUP BY
                data_coleta
                , marca
        )
        SELECT
            marca AS marca
            , AVG(porcentagem) AS porcentagem
            , periodo AS periodo
        FROM
            porcentagem_por_dia
        GROUP BY
            marca;
    """

    return query


def macro_preco_medio_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO preco_medio_e_num_produtos_periodo(data_inicio, data_fim) AS TABLE
        WITH preco_medio_por_dia AS (
            SELECT
                marca AS marca
                , AVG(preco_atual) AS preco_medio
                , COUNT(*) AS num_produtos
            FROM
                dados_completos_por_periodo(data_inicio, data_fim)
            GROUP BY
                data_coleta
                , marca
        )
        SELECT
            marca
            , AVG(preco_medio) AS preco_medio
            , AVG(num_produtos) AS num_produtos
        FROM
            preco_medio_por_dia
        GROUP BY
            marca;
    """

    return query


def macro_faixa_preco_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO faixa_preco_periodo(data_inicio, data_fim) AS TABLE
        WITH faixa_preco_por_dia AS (
            SELECT
                marca AS marca
                , CASE
                    WHEN preco_atual < 200 THEN '200'
                    WHEN preco_atual BETWEEN 200 AND 400 THEN '200_400'
                    ELSE '400'
                  END AS faixa_preco
                , COUNT(*) AS num_produtos
            FROM
                dados_completos_por_periodo(data_inicio, data_fim)
            GROUP BY
                data_coleta
                , marca
                , faixa_preco
        )
        SELECT
            marca
            , faixa_preco
            , AVG(num_produtos) AS num_produtos
        FROM
            faixa_preco_por_dia
        GROUP BY
            marca
            , faixa_preco;
    """

    return query


def macro_media_avaliacoes_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO media_avaliacoes_periodo(data_inicio, data_fim) AS TABLE
        WITH media_avaliacoes_por_dia AS (
            SELECT
                marca AS marca
                , AVG(nota_avaliacao) AS media_avaliacao
                , AVG(num_avaliacoes) AS media_num_avaliacoes
            FROM
                dados_completos_por_periodo(data_inicio, data_fim)
            GROUP BY
                data_coleta
                , marca
        )
        SELECT
            marca
            , AVG(media_avaliacao) AS avaliacao
            , AVG(media_num_avaliacoes) AS num_avaliacoes
        FROM
            media_avaliacoes_por_dia
        GROUP BY
            marca;
    """

    return query
