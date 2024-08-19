import duckdb


def conexao_db_local() -> duckdb.DuckDBPyConnection:
    conexao = duckdb.connect("../db_auxiliar.db")

    return conexao


def criar_tabela(conexao: duckdb.DuckDBPyConnection) -> None:
    query = """
        create table if not exists arquivos_salvos (
            arquivo varchar(255) not null
            , horario varchar(255) not null
        );
    """

    conexao.sql(query)


def retorna_arquivos_salvos(conexao: duckdb.DuckDBPyConnection) -> list[str]:
    query = """
        select
            arquivo
        from
            arquivos_salvos;
    """

    lista = [linha[0] for linha in conexao.sql(query).fetchall()]

    return lista


def verifica_se_arquivo_ja_foi_salvo(nome_arquivo: str) -> bool:
    with conexao_db_local() as conexao:
        criar_tabela(conexao)
        lista_arquivos_salvos = retorna_arquivos_salvos(conexao)

    return nome_arquivo in lista_arquivos_salvos


def inserir_arquivo(nome_arquivo: str, horario: str) -> None:
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
