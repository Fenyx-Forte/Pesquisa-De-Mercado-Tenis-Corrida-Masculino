from duckdb import DuckDBPyConnection


class EscopoGlobal:
    conexao: DuckDBPyConnection
    cabecalho_data_coleta: str
    data_coleta_mais_recente: str
    data_6_dias_atras: str
    data_coleta_mais_antiga: str

    def __init__(
        self,
        conexao: DuckDBPyConnection,
        cabecalho_data_coleta: str,
        data_coleta_mais_recente: str,
        data_6_dias_atras: str,
        data_coleta_mais_antiga: str,
    ) -> None:
        self.conexao = conexao
        self.cabecalho_data_coleta = cabecalho_data_coleta
        self.data_coleta_mais_recente = data_coleta_mais_recente
        self.data_6_dias_atras = data_6_dias_atras
        self.data_coleta_mais_antiga = data_coleta_mais_antiga
