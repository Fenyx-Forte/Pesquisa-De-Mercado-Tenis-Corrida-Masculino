from duckdb import DuckDBPyConnection

from dashboard.processamento.queries import pagina_7_queries


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


def dados_hoje(conexao: DuckDBPyConnection) -> list[dict]:
    query = pagina_7_queries.query_promocao_hoje()

    return conexao.sql(query).df().to_dict(orient="records")


def dados_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
) -> list[dict]:
    query = pagina_7_queries.query_promocao_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return conexao.execute(query, parametros).df().to_dict(orient="records")


def retorna_periodo_novo(
    data_inicio: str,
    data_fim: str,
):
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    return f"{data_inicio_formatada} - {data_fim_formatada}"
