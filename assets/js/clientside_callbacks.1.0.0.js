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
                return "coluna-sidebar-ativada";
            }

            return "coluna-sidebar-desativada";
        },

        fechar_sidebar: function(url_atual) {
            return "coluna-sidebar-desativada";
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
            let valor1 = str1.replace("R$ ", "").replace("%", "");
            let valor2 = str2.replace("R$ ", "").replace("%", "");
            let valor3 = str3.replace("R$ ", "").replace("%", "");

            let numbers = [parseFloat(valor1), parseFloat(valor2), parseFloat(valor3)];

            let sortedUnique = [...new Set(numbers.slice().sort((a, b) => b - a))];

            return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
        },

        ranking_inverso: function(str1, str2, str3) {
            let valor1 = str1.replace("R$ ", "").replace("%", "");
            let valor2 = str2.replace("R$ ", "").replace("%", "");
            let valor3 = str3.replace("R$ ", "").replace("%", "");

            let numbers = [parseFloat(valor1), parseFloat(valor2), parseFloat(valor3)];

            let sortedUnique = [...new Set(numbers.slice().sort((a, b) => a - b))];

            return numbers.map(num => `ranking_top_${sortedUnique.indexOf(num) + 1}`);
        },

        linha_totais_preco_medio: function(lista_dados, dash_grid_options) {
            let num_marcas = lista_dados.length;
            let soma_num_produtos = 0;
            let media_preco_medio = 0;

            if (num_marcas === 0) {
                return {
                    ...dash_grid_options,
                    pinnedBottomRowData: [{
                        marca: num_marcas,
                        num_produtos: soma_num_produtos,
                        preco_medio: media_preco_medio
                    }]
                }
            }

            let total_preco_medio = 0;

            lista_dados.forEach(dado => {
                soma_num_produtos += dado["num_produtos"];
                total_preco_medio += dado["preco_medio"] * dado["num_produtos"];
            });

            media_preco_medio = total_preco_medio / soma_num_produtos;

            return {
                ...dash_grid_options,
                pinnedBottomRowData: [{
                    marca: num_marcas,
                    num_produtos: soma_num_produtos,
                    preco_medio: media_preco_medio
                }]
            };
        },

        linha_totais_faixa_preco: function(lista_dados, dash_grid_options) {
            let num_marcas = lista_dados.length;
            let soma_num_produtos = 0;

            if (num_marcas === 0) {
                return {
                    ...dash_grid_options,
                    pinnedBottomRowData: [{
                        marca: num_marcas,
                        num_produtos: soma_num_produtos
                    }]
                }
            }

            lista_dados.forEach(dado => {
                soma_num_produtos += dado["num_produtos"];
            });

            return {
                ...dash_grid_options,
                pinnedBottomRowData: [{
                    marca: num_marcas,
                    num_produtos: soma_num_produtos
                }]
            };
        },

        linha_totais_satisfacao: function(lista_dados, dash_grid_options) {
            let num_marcas = lista_dados.length;
            let soma_num_avaliacoes = 0;
            let media_nota_avaliacao = 0;

            if (num_marcas === 0) {
                return {
                    ...dash_grid_options,
                    pinnedBottomRowData: [{
                        marca: num_marcas,
                        num_avaliacoes: soma_num_avaliacoes,
                        nota_avaliacao: media_nota_avaliacao
                    }]
                }
            }

            let total_nota_avaliacao = 0;

            lista_dados.forEach(dado => {
                soma_num_avaliacoes += dado["num_avaliacoes"];
                total_nota_avaliacao += dado["nota_avaliacao"] * dado["num_avaliacoes"];
            });

            media_nota_avaliacao = total_nota_avaliacao / soma_num_avaliacoes;

            return {
                ...dash_grid_options,
                pinnedBottomRowData: [{
                    marca: num_marcas,
                    num_avaliacoes: soma_num_avaliacoes,
                    nota_avaliacao: media_nota_avaliacao
                }]
            };
        },

        linha_totais_promocoes: function(lista_dados, dash_grid_options) {
            let num_marcas = lista_dados.length;
            let soma_produtos = 0;
            let media_desconto = 0;

            if (num_marcas === 0) {
                return {
                    ...dash_grid_options,
                    pinnedBottomRowData: [{
                        marca: num_marcas,
                        produtos: soma_produtos,
                        desconto: media_desconto
                    }]
                }
            }

            let total_desconto = 0;

            lista_dados.forEach(dado => {
                soma_produtos += dado["produtos"];
                total_desconto += dado["desconto"] * dado["produtos"];
            });

            media_desconto = total_desconto / soma_produtos;

            return {
                ...dash_grid_options,
                pinnedBottomRowData: [{
                    marca: num_marcas,
                    produtos: soma_produtos,
                    desconto: media_desconto
                }]
            };
        }
    }
}
);
