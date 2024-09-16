from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame

from dashboard.processamento.queries import pagina_4_queries


def callback_verificar_datas() -> str:
    funcao = """
    function verificar_datas(n_clicks, data_inicio, data_fim, periodo_hoje, periodo_ja_escolhido, periodo_historico) {
        if (!data_inicio || !data_fim) {
            return ["Período Inválido", "Selecione as datas usando o calendário ou escreva as datas no formato DD/MM/YYYY."];
        }

        function formatar_data(data) {
            const [ano, mes, dia] = data.split('-');
            return `${dia}/${mes}/${ano}`;
        }

        const data_inicio_formatada = formatar_data(data_inicio);
        const data_fim_formatada = formatar_data(data_fim);

        const periodo = `${data_inicio_formatada} - ${data_fim_formatada}`;

        if (periodo === periodo_hoje || periodo === periodo_ja_escolhido || periodo === periodo_historico) {
            return ["Período Já Adicionado", "Esse período já foi adicionado. Adicione um período diferente."];
        }

        return ["", ""];
    }
    """

    return funcao


def callback_abrir_modal() -> str:
    funcao = """
    function abrirModal(titulo) {
        if (titulo === "") {
            return window.dash_clientside.no_update;
        }
        return true;
    }
    """

    return funcao


def formatar_data_pt_br(data: str) -> str:
    # "data" esta no formato YYYY-MM-DD
    componentes = data.split("-")
    dia = componentes[2]
    mes = componentes[1]
    ano = componentes[0]

    return f"{dia}/{mes}/{ano}"


def dados_abaixo_de_200(df: pd_DataFrame) -> pd_DataFrame:
    return pd_DataFrame()


def dados_entre_200_e_400_(df: pd_DataFrame) -> pd_DataFrame:
    return pd_DataFrame()


def dados_acima_de_400_(df: pd_DataFrame) -> pd_DataFrame:
    return pd_DataFrame()


def dados_hoje(conexao: DuckDBPyConnection) -> list[list[dict]]:
    df_hoje = pd_DataFrame()

    df_abaixo_de_200 = dados_abaixo_de_200(df_hoje)

    df_entre_200_e_400 = dados_entre_200_e_400_(df_hoje)

    df_acima_de_400 = dados_acima_de_400_(df_hoje)

    return [
        df_abaixo_de_200.to_dict("records"),
        df_entre_200_e_400.to_dict("records"),
        df_acima_de_400.to_dict("records"),
    ]


def dados_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> list[list[dict]]:
    df_periodo = pd_DataFrame()

    df_abaixo_de_200 = dados_abaixo_de_200(df_periodo)

    df_entre_200_e_400 = dados_entre_200_e_400_(df_periodo)

    df_acima_de_400 = dados_acima_de_400_(df_periodo)

    return [
        df_abaixo_de_200.to_dict("records"),
        df_entre_200_e_400.to_dict("records"),
        df_acima_de_400.to_dict("records"),
    ]
