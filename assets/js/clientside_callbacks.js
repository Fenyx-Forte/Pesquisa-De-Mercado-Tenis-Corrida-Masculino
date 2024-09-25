window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        atualizar_titulo_pagina: function(url_atual) {
            const titulos = {
                "/": "Home",
                "/kpis": "KPI's",
                "/top-10-marcas-atuais": "Top 10 Marcas Atuais",
                "/top-10-marcas-periodo": "Top 10 Marcas Período",
                "/preco-medio": "Preço Médio",
                "/faixa-preco": "Faixa Preço",
                "/satisfacao": "Satisfação",
                "/promocoes": "Promoções"
            };

            document.title = titulos[url_atual] || "Not Found 404";
        },

        abrir_e_fechar_sidebar: function(n_clicks) {
            if (n_clicks % 2 === 1) {
                return "minha-sidebar-escondida";
            }

            return "minha-sidebar";
        },

        verificar_datas: function(n_clicks, data_inicio, data_fim, periodo_hoje, periodo_ja_escolhido, periodo_historico) {
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
        },

        abrir_modal: function(titulo) {
            if (titulo === "") {
                return window.dash_clientside.no_update;
            }
            return true;
        },

        ranking_direto: function(str1, str2, str3) {
            let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

            let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

            return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
        },

        ranking_inverso: function(str1, str2, str3) {
            let numbers = [parseFloat(str1), parseFloat(str2), parseFloat(str3)];

            let sortedUnique = [...new Set(numbers.slice().sort((a, b) => a - b))];

            return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
        }
    }
}
);
