from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame


def verifica_se_datas_sao_validas(data_inicio: str, data_fim: str) -> bool:
    if (data_inicio is None) or (data_fim is None):
        return False

    return True


def verifica_se_periodo_ja_foi_adicionado(
    data_inicio: str,
    data_fim: str,
    periodo_hoje: str,
    periodo_ja_escolhido: str,
    periodo_historico: str,
) -> bool:
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    periodo = f"{data_inicio_formatada} - {data_fim_formatada}"

    return periodo in [periodo_hoje, periodo_ja_escolhido, periodo_historico]


def formatar_data_pt_br(data: str) -> str:
    # "data" esta no formato YYYY/MM/DD
    componentes = data.split("-")
    dia = componentes[2]
    mes = componentes[1]
    ano = componentes[0]

    return f"{dia}/{mes}/{ano}"
