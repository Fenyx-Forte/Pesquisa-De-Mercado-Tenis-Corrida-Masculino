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


def callback_ranking_direto_valores() -> str:
    funcao = """
    function ranking_direto(str1, str2, str3) {
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
    }
    """

    return funcao


def callback_ranking_inverso_valores() -> str:
    funcao = """
    function ranking_inverso(str1, str2, str3) {
        let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

        let sortedUnique = [...new Set(numbers.slice().sort((a, b) => a - b))];

        return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
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


def retorna_periodo(data_inicio: str, data_fim: str) -> str:
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    return f"{data_inicio_formatada} - {data_fim_formatada}"
