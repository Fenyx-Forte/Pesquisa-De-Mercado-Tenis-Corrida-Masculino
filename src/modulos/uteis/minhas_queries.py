def dados_mais_recentes_do_banco_de_dados() -> str:
    query = """
    SELECT
        marca
        , produto
        , preco_velho
        , preco_atual
        , promocao
        , percentual_promocao
        , nota_avaliacao
        , num_avaliacoes
        , _data_coleta
        , _horario_coleta
        , _pagina
        , _ordem
    FROM
        db.mercado_livre AS ml
    WHERE
        "_data_coleta" = (
            SELECT
                MAX("_data_coleta")
            FROM
                db.mercado_livre
        );
    """

    return query


def data_coleta_mais_recente() -> str:
    query = """
    SELECT
        STRFTIME(_data_coleta, '%d/%m/%Y')
        , _horario_coleta
    FROM
        df
    LIMIT
        1;
    """

    return query


def kpi_num_total_itens() -> str:
    query = """
    SELECT
        count(*) AS "Número Total de Produtos"
    FROM
        df;
    """

    return query


def kpi_num_marcas_unicas() -> str:
    query = """
    SELECT
        COUNT(DISTINCT marca) AS "Número de Marcas"
    FROM
        df
    WHERE
        marca <> 'GENERICA';
    """

    return query


def kpi_preco_atual_medio() -> str:
    query = """
    SELECT
        AVG(preco_atual) AS "Média Preço"
    FROM
        df;
    """

    return query


def marcas_mais_encontradas() -> str:
    query = """
    SELECT
        marca AS "Marca"
        , COUNT(marca) AS "Qtd Produtos"
    FROM
        df
    GROUP BY
        marca
    ORDER BY
        "Qtd Produtos" DESC
        , marca ASC
    LIMIT
        10;
    """

    return query


def preco_medio_por_marca() -> str:
    query = """
    SELECT
        marcas as "Marca"
        , AVG(preco_atual) AS "Preço Médio"
    FROM
        df
    GROUP BY
        marca
    ORDER BY
        "Preço Médio" DESC
        , marca ASC;
    """

    return query


def satisfacao_media_por_marca() -> str:
    query = """
    SELECT
        marca as "Marca"
        , AVG(nota_avalicao) as "Satisfação Média"
    FROM
        df
    WHERE
        num_avaliacoes >= 20
    GROUP BY
        marca
    ORDER BY
        "Satisfação Média" DESC
        , marca ASC;
    """

    return query