from duckdb import connect


def instalar_extensao_postgresql():
    instalacao = """
        INSTALL postgres;
    """

    with connect(":memory:") as conexao:
        conexao.sql(instalacao)


if __name__ == "__main__":
    instalar_extensao_postgresql()
