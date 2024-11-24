def tabela_dados_completos() -> str:
    query = """
    CREATE TABLE
        dados_completos AS
    SELECT
        marca
        , produto
        , preco_velho
        , preco_atual
        , promocao
        , percentual_promocao
        , nota_avaliacao
        , num_avaliacoes
        , data_coleta
        , horario_coleta
        , pagina
        , ordem
    FROM
        db.view_tenis_corrida;

    DETACH db;
    """

    return query


def tabela_dados_mais_recentes() -> str:
    query = """
    CREATE TABLE
        dados_mais_recentes AS
    SELECT
        marca
        , produto
        , preco_velho
        , preco_atual
        , promocao
        , percentual_promocao
        , nota_avaliacao
        , num_avaliacoes
        , data_coleta
        , horario_coleta
        , pagina
        , ordem
    FROM
        dados_completos AS dc
    WHERE
        dc.data_coleta = (
            SELECT
                MAX(data_coleta)
            FROM
                dados_completos
        );
    """

    return query
