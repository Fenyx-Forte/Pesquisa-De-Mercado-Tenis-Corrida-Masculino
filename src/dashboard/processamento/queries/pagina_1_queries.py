def query_numero_produtos_e_media_precos_hoje() -> str:
    query = """
    SELECT
        COUNT(*) as numero_produtos
        , FORMAT('{:.2f}', AVG(preco_atual)) as media_precos
    FROM
        dados_mais_recentes;
    """

    return query


def query_media_produtos_e_media_precos_periodo() -> str:
    query = """
    WITH produtos_e_preco_medio_por_dia AS (
        SELECT
            COUNT(*) as numero_produtos
            , AVG(preco_atual) as media_precos
        FROM
            dados_completos_por_periodo($data_inicio, $data_fim)
        GROUP BY
            data_coleta
    )
    SELECT
        FORMAT('{:.2f}', AVG(numero_produtos)) as media_produtos_por_dia
        , FORMAT('{:.2f}', AVG(media_precos)) as media_precos_por_dia
    FROM
        produtos_e_preco_medio_por_dia;
    """

    return query


def query_numero_marcas_hoje() -> str:
    query = """
    SELECT
        COUNT(DISTINCT marca) as numero_marcas
    FROM
        dados_mais_recentes
    WHERE
        marca <> 'GENERICA';
    """

    return query


def query_media_marcas_periodo() -> str:
    query = """
    WITH marcas_por_dia AS (
        SELECT
            COUNT(DISTINCT marca) as numero_marcas
        FROM
            dados_completos_por_periodo($data_inicio, $data_fim)
        WHERE
            marca <> 'GENERICA'
        GROUP BY
            data_coleta
    )
    SELECT
        FORMAT('{:.2f}', AVG(numero_marcas)) as media_marcas_por_dia
    FROM
        marcas_por_dia;
    """

    return query


def query_numero_produtos_em_promocao_e_percentual_medio_desconto_hoje() -> str:
    query = """
    SELECT
        COUNT(*) as numero_produtos_em_promocao
        , FORMAT('{:.2f}', AVG(percentual_promocao) * 100) as percentual_medio_desconto
    FROM
        dados_mais_recentes
    WHERE
        promocao = true;
    """

    return query


def query_media_produtos_em_promocao_e_media_percentual_desconto_periodo() -> (
    str
):
    query = """
    WITH produtos_em_promocao_e_percentual_desconto_por_dia AS (
        SELECT
            COUNT(*) as numero_produtos_em_promocao
            , AVG(percentual_promocao) as percentual_medio_desconto
        FROM
            dados_completos_por_periodo($data_inicio, $data_fim)
        WHERE
            promocao = true
        GROUP BY
            data_coleta
    )
    SELECT
        FORMAT('{:.2f}', AVG(numero_produtos_em_promocao)) as media_produtos_em_promocao
        , FORMAT('{:.2f}', AVG(percentual_medio_desconto) * 100) as media_percentual_desconto
    FROM
        produtos_em_promocao_e_percentual_desconto_por_dia;
    """

    return query


def query_numero_marcas_em_promocao_hoje() -> str:
    query = """
    SELECT
        COUNT(DISTINCT marca) as numero_marcas_em_promocao
    FROM
        dados_mais_recentes
    WHERE
        promocao = true
        AND marca <> 'GENERICA';
    """

    return query


def query_media_marcas_em_promocao_periodo() -> str:
    query = """
    WITH marcas_em_promocao_por_dia AS (
        SELECT
            COUNT(DISTINCT marca) as numero_marcas_em_promocao
        FROM
            dados_completos_por_periodo($data_inicio, $data_fim)
        WHERE
            promocao = true
            AND marca <> 'GENERICA'
        GROUP BY
            data_coleta
    )
    SELECT
        FORMAT('{:.2f}', AVG(numero_marcas_em_promocao)) as media_marcas_em_promocao
    FROM
        marcas_em_promocao_por_dia;
    """

    return query


def query_numero_produtos_abaixo_de_200_reais_hoje() -> str:
    query = """
    SELECT
        COUNT(*) as numero_produtos_abaixo_de_200_reais
    FROM
        dados_mais_recentes
    WHERE
        preco_atual < 200;
    """

    return query


def query_media_produtos_abaixo_de_200_reais_periodo() -> str:
    query = """
    WITH produtos_abaixo_de_200_reais_por_dia AS (
        SELECT
            COUNT(*) as numero_produtos_abaixo_de_200_reais
        FROM
            dados_completos_por_periodo($data_inicio, $data_fim)
        WHERE
            preco_atual < 200
        GROUP BY
            data_coleta
    )
    SELECT
        FORMAT('{:.2f}', AVG(numero_produtos_abaixo_de_200_reais)) as media_produtos_abaixo_de_200_reais
    FROM
        produtos_abaixo_de_200_reais_por_dia;
    """

    return query


def query_numero_produtos_com_20_ou_mais_avaliacoes_hoje() -> str:
    query = """
    SELECT
        COUNT(*) as numero_produtos_com_20_ou_mais_avaliacoes
    FROM
        dados_mais_recentes
    WHERE
        num_avaliacoes >= 20;
    """

    return query


def query_media_produtos_com_20_ou_mais_avaliacoes_periodo() -> str:
    query = """
    WITH produtos_com_20_ou_mais_avaliacoes_por_dia AS (
        SELECT
            COUNT(*) as numero_produtos_com_20_ou_mais_avaliacoes
        FROM
            dados_completos_por_periodo($data_inicio, $data_fim)
        WHERE
            num_avaliacoes >= 20
        GROUP BY
            data_coleta
    )

    SELECT
        FORMAT('{:.2f}', AVG(numero_produtos_com_20_ou_mais_avaliacoes)) as media_produtos_com_20_ou_mais_avaliacoes
    FROM
        produtos_com_20_ou_mais_avaliacoes_por_dia;
    """

    return query


def query_numero_produtos_sem_avaliacoes_hoje() -> str:
    query = """
    SELECT
        COUNT(*) as numero_produtos_sem_avaliacoes
    FROM
        dados_mais_recentes
    WHERE
        num_avaliacoes = 0;
    """

    return query


def query_media_produtos_sem_avaliacoes_periodo() -> str:
    query = """
    WITH produtos_sem_avaliacoes_por_dia AS (
        SELECT
            COUNT(*) as numero_produtos_sem_avaliacoes
        FROM
            dados_completos_por_periodo($data_inicio, $data_fim)
        WHERE
            num_avaliacoes = 0
        GROUP BY
            data_coleta
    )
    SELECT
        FORMAT('{:.2f}', AVG(numero_produtos_sem_avaliacoes)) as media_produtos_sem_avaliacoes
    FROM
        produtos_sem_avaliacoes_por_dia;
    """

    return query


def query_numero_produtos_com_nota_superior_4_hoje() -> str:
    query = """
    SELECT
        COUNT(*) as numero_produtos_com_nota_superior_4
    FROM
        dados_mais_recentes
    WHERE
        num_avaliacoes > 0
        AND nota_avaliacao > 4;
    """

    return query


def query_media_produtos_com_nota_superior_4_periodo() -> str:
    query = """
    WITH produtos_com_nota_superior_4_por_dia AS (
        SELECT
            COUNT(*) as numero_produtos_com_nota_superior_4
        FROM
            dados_completos_por_periodo($data_inicio, $data_fim)
        WHERE
            num_avaliacoes > 0
            AND nota_avaliacao > 4
        GROUP BY
            data_coleta
    )
    SELECT
        FORMAT('{:.2f}', AVG(numero_produtos_com_nota_superior_4)) as media_produtos_com_nota_superior_4
    FROM
        produtos_com_nota_superior_4_por_dia;
    """

    return query
