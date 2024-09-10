def tabela_dados_completos() -> str:
    query = """
    CREATE TABLE
        dados_completos AS
    SELECT
        *
    FROM
        db.view_dados_completos;

    DETACH db;
    """

    return query


def tabela_dados_mais_recentes() -> str:
    query = """
    CREATE TABLE
        dados_mais_recentes AS
    SELECT
        *
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
