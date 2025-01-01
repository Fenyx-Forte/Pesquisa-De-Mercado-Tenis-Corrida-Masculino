"""Este arquivo contém funções que são usadas para manipular o banco de dados local."""

import duckdb


def conexao_db_local() -> duckdb.DuckDBPyConnection:
    """Cria uma conexão com o banco de dados local.

    Returns:
        duckdb.DuckDBPyConnection: Conexão com o banco de dados local.
    """
    return duckdb.connect("../db_auxiliar.db")


def criar_tabela(conexao: duckdb.DuckDBPyConnection) -> None:
    """Cria a tabela de arquivos salvos no banco de dados local.

    Args:
        conexao (duckdb.DuckDBPyConnection): Conexão com o banco de dados local.
    """
    query = """
        create table if not exists arquivos_salvos (
            arquivo varchar(255) not null
            , horario varchar(255) not null
        );
    """

    conexao.sql(query)


def retorna_arquivos_salvos(conexao: duckdb.DuckDBPyConnection) -> list[str]:
    """Retorna a lista de arquivos salvos no banco de dados local.

    Args:
        conexao (duckdb.DuckDBPyConnection): Conexão com o banco de dados local.

    Returns:
        list[str]: Lista de arquivos salvos no banco de dados local.
    """
    query = """
        select
            arquivo
        from
            arquivos_salvos;
    """

    return [linha[0] for linha in conexao.sql(query).fetchall()]


def verifica_se_arquivo_ja_foi_salvo(nome_arquivo: str) -> bool:
    """Verifica se o arquivo já foi salvo no banco de dados local.

    Args:
        nome_arquivo (str): Nome do arquivo a ser verificado.

    Returns:
        bool: True se o arquivo já foi salvo no banco de dados local, False caso contrário.
    """
    with conexao_db_local() as conexao:
        criar_tabela(conexao)
        lista_arquivos_salvos = retorna_arquivos_salvos(conexao)

    return nome_arquivo in lista_arquivos_salvos


def inserir_arquivo(nome_arquivo: str, horario: str) -> None:
    """Insere um arquivo no banco de dados local.

    Args:
        nome_arquivo (str): Nome do arquivo a ser inserido.
        horario (str): Horário em que o arquivo foi salvo.
    """
    query = """
        insert into arquivos_salvos values (
            $arquivo, $horario
        );
    """

    parametros = {
        "arquivo": nome_arquivo,
        "horario": horario,
    }

    with conexao_db_local() as conexao:
        criar_tabela(conexao)
        conexao.execute(query, parametros)
