from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame
from pandas import concat as pd_concat

from dashboard.processamento.queries import pagina_2_queries


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


def top_10_marcas_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
    lista_marcas: list[str],
) -> pd_DataFrame:
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    periodo = f"{data_inicio_formatada} - {data_fim_formatada}"

    query = pagina_2_queries.query_top_10_marcas_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "periodo": periodo,
        "lista_marcas": lista_marcas,
    }

    return conexao.execute(query, parametros).df()


def inicializa_top_10_marcas_atuais(
    conexao: DuckDBPyConnection,
    data_coleta_mais_recente: str,
    data_6_dias_atras: str,
    data_coleta_mais_antiga: str,
    df_hoje: pd_DataFrame,
) -> pd_DataFrame:
    lista_marcas = df_hoje["Marca"].tolist()

    df_ultima_semana = top_10_marcas_periodo(
        conexao, data_6_dias_atras, data_coleta_mais_recente, lista_marcas
    )

    df_historico = top_10_marcas_periodo(
        conexao, data_coleta_mais_antiga, data_coleta_mais_recente, lista_marcas
    )

    return pd_concat([df_hoje, df_ultima_semana, df_historico])


def dataframe_a_partir_dados_grafico(
    dados_grafico_atual: dict[str, list[dict]], i: int, qtd_itens: int
):
    return pd_DataFrame(
        {
            "Marca": dados_grafico_atual["data"][i]["x"],
            "Porcentagem": dados_grafico_atual["data"][i]["y"],
            "Periodo": [
                dados_grafico_atual["data"][i]["legendgroup"]
                for n in range(qtd_itens)
            ],
        }
    )


def dados_grafico_atualizado(
    conexao: DuckDBPyConnection,
    dados_grafico_atual: dict[str, list[dict]],
    data_inicio: str,
    data_fim: str,
):
    lista_marcas = dados_grafico_atual["data"][0]["x"]

    qtd_itens = len(lista_marcas)

    df_hoje = dataframe_a_partir_dados_grafico(
        dados_grafico_atual, 0, qtd_itens
    )

    df_novo = top_10_marcas_periodo(
        conexao, data_inicio, data_fim, lista_marcas
    )

    df_historico = dataframe_a_partir_dados_grafico(
        dados_grafico_atual, 2, qtd_itens
    )

    return pd_concat([df_hoje, df_novo, df_historico])


def retorna_periodo_novo(data_inicio: str, data_fim: str):
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    return f"{data_inicio_formatada} - {data_fim_formatada}"
