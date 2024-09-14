from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame


class EscopoGlobal:
    conexao: DuckDBPyConnection
    cabecalho_data_coleta: str
    data_coleta_mais_recente: str
    data_6_dias_atras: str
    data_coleta_mais_antiga: str
    df_top_10_marcas_hoje: pd_DataFrame

    def __init__(
        self,
        conexao: DuckDBPyConnection,
        cabecalho_data_coleta: str,
        data_coleta_mais_recente: str,
        data_6_dias_atras: str,
        data_coleta_mais_antiga: str,
        df_top_10_marcas_hoje: pd_DataFrame,
    ) -> None:
        self.conexao = conexao
        self.cabecalho_data_coleta = cabecalho_data_coleta
        self.data_coleta_mais_recente = data_coleta_mais_recente
        self.data_6_dias_atras = data_6_dias_atras
        self.data_coleta_mais_antiga = data_coleta_mais_antiga
        self.df_top_10_marcas_hoje = df_top_10_marcas_hoje
