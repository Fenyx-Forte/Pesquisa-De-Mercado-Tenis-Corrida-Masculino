from dash import html
from dash_bootstrap_components import Card, CardBody
from duckdb import DuckDBPyConnection

from dashboard.processamento.queries import pagina_1_queries


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


def numero_produtos_hoje(conexao: DuckDBPyConnection) -> str:
    query = pagina_1_queries.query_numero_produtos_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_produtos_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_marcas_hoje(conexao: DuckDBPyConnection) -> str:
    query = pagina_1_queries.query_numero_marcas_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_marcas_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_marcas_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_em_promocao_hoje(conexao: DuckDBPyConnection) -> str:
    query = pagina_1_queries.query_numero_produtos_em_promocao_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_em_promocao_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_produtos_em_promocao_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_marcas_em_promocao_hoje(conexao: DuckDBPyConnection) -> str:
    query = pagina_1_queries.query_numero_marcas_em_promocao_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_marcas_em_promocao_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_marcas_em_promocao_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def percentual_medio_desconto_hoje(conexao: DuckDBPyConnection) -> str:
    query = pagina_1_queries.query_percentual_medio_desconto_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_percentual_desconto_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_percentual_desconto_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def media_precos_hoje(conexao: DuckDBPyConnection) -> str:
    query = pagina_1_queries.query_media_precos_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_precos_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_precos_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_abaixo_de_200_reais_hoje(
    conexao: DuckDBPyConnection,
) -> str:
    query = pagina_1_queries.query_numero_produtos_abaixo_de_200_reais_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_abaixo_de_200_reais_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_produtos_abaixo_de_200_reais_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_com_20_ou_mais_avaliacoes_hoje(
    conexao: DuckDBPyConnection,
) -> str:
    query = (
        pagina_1_queries.query_numero_produtos_com_20_ou_mais_avaliacoes_hoje()
    )

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_com_20_ou_mais_avaliacoes_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_produtos_com_20_ou_mais_avaliacoes_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_sem_avaliacoes_hoje(conexao: DuckDBPyConnection) -> str:
    query = pagina_1_queries.query_numero_produtos_sem_avaliacoes_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_sem_avaliacoes_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_produtos_sem_avaliacoes_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_com_nota_superior_4_hoje(
    conexao: DuckDBPyConnection,
) -> str:
    query = pagina_1_queries.query_numero_produtos_com_nota_superior_4_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_com_nota_superior_4_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = pagina_1_queries.query_media_produtos_com_nota_superior_4_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def cartao(titulo: str, valor: str, id_valor: str, id_ranking: str) -> Card:
    conteudo = Card(
        CardBody(
            [
                html.Div(
                    titulo,
                    className="titulo_cartao",
                ),
                html.Div(
                    valor,
                    className="valor_cartao",
                    id=id_valor,
                ),
                html.Div(
                    html.I(className="fa-solid fa-trophy"),
                    id=id_ranking,
                ),
            ]
        )
    )

    return conteudo


def div_cartao(
    titulo: str, valor: str, id_valor: str, id_ranking: str
) -> html.Div:
    conteudo = html.Div(
        cartao(
            titulo,
            valor,
            id_valor,
            id_ranking,
        ),
        className="div_card",
    )

    return conteudo


def cartao_num_produtos(valor: str, sufixo: str) -> html.Div:
    titulo = "Número Produtos"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_num_produtos_{sufixo}",
        id_ranking=f"pagina_1_ranking_num_produtos_{sufixo}",
    )

    return conteudo


def cartao_num_marcas(valor: str, sufixo: str) -> html.Div:
    titulo = "Número Marcas"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_num_marcas_{sufixo}",
        id_ranking=f"pagina_1_ranking_num_marcas_{sufixo}",
    )

    return conteudo


def cartao_num_produtos_promocoes(valor: str, sufixo: str) -> html.Div:
    titulo = "Produtos Em Promocão"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_num_produtos_promocoes_{sufixo}",
        id_ranking=f"pagina_1_ranking_num_produtos_promocoes_{sufixo}",
    )

    return conteudo


def cartao_num_marcas_promocoes(valor: str, sufixo: str) -> html.Div:
    titulo = "Marcas Em Promoção"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_num_marcas_promocoes_{sufixo}",
        id_ranking=f"pagina_1_ranking_num_marcas_promocoes_{sufixo}",
    )

    return conteudo


def cartao_produtos_abaixo_de_200_reais(valor: str, sufixo: str) -> html.Div:
    titulo = "Produtos Abaixo De R$ 200,00"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_produtos_abaixo_200_{sufixo}",
        id_ranking=f"pagina_1_ranking_produtos_abaixo_200_{sufixo}",
    )

    return conteudo


def cartao_percentual_medio_desconto(valor: str, sufixo: str) -> html.Div:
    titulo = "% Média Desconto"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_percentual_medio_desconto_{sufixo}",
        id_ranking=f"pagina_1_ranking_percentual_medio_desconto_{sufixo}",
    )

    return conteudo


def cartao_media_precos(valor: str, sufixo: str) -> html.Div:
    titulo = "Média Preços"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_media_precos_{sufixo}",
        id_ranking=f"pagina_1_ranking_media_precos_{sufixo}",
    )

    return conteudo


def cartao_produtos_com_mais_20_avaliacoes(valor: str, sufixo: str) -> html.Div:
    titulo = "Produtos Com 20 Ou Mais Avaliações"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_num_produtos_20_ou_mais_avaliacoes_{sufixo}",
        id_ranking=f"pagina_1_ranking_num_produtos_20_ou_mais_avaliacoes_{sufixo}",
    )

    return conteudo


def cartao_produtos_sem_avaliacao(valor: str, sufixo: str) -> html.Div:
    titulo = "Produtos Sem Avaliações"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_num_produtos_sem_avaliacoes_{sufixo}",
        id_ranking=f"pagina_1_ranking_num_produtos_sem_avaliacoes_{sufixo}",
    )

    return conteudo


def cartao_produtos_com_nota_maior_que_4(valor: str, sufixo: str) -> html.Div:
    titulo = "Produtos Com Nota Maior Que 4"

    conteudo = div_cartao(
        titulo=titulo,
        valor=valor,
        id_valor=f"pagina_1_valor_num_produtos_nota_maior_4_{sufixo}",
        id_ranking=f"pagina_1_ranking_num_produtos_nota_maior_4_{sufixo}",
    )

    return conteudo


def informacoes_coluna(
    div_cartao_num_produtos: html.Div,
    div_cartao_num_marcas: html.Div,
    div_cartao_media_precos: html.Div,
    div_cartao_num_produtos_promocoes: html.Div,
    div_cartao_num_marcas_promocoes: html.Div,
    div_cartao_percentual_medio_desconto: html.Div,
    div_cartao_num_produtos_abaixo_200_reais: html.Div,
    div_cartao_produtos_com_mais_20_avaliacoes: html.Div,
    div_cartao_produtos_sem_avaliacao: html.Div,
    div_cartao_produtos_com_nota_maior_que_4: html.Div,
) -> html.Div:
    conteudo = html.Div(
        [
            div_cartao_num_produtos,
            html.Br(),
            div_cartao_num_marcas,
            html.Br(),
            div_cartao_media_precos,
            html.Br(),
            div_cartao_num_produtos_promocoes,
            html.Br(),
            div_cartao_num_marcas_promocoes,
            html.Br(),
            div_cartao_percentual_medio_desconto,
            html.Br(),
            div_cartao_num_produtos_abaixo_200_reais,
            html.Br(),
            div_cartao_produtos_com_nota_maior_que_4,
            html.Br(),
            div_cartao_produtos_com_mais_20_avaliacoes,
            html.Br(),
            div_cartao_produtos_sem_avaliacao,
            html.Br(),
        ],
        className="informacoes_coluna",
    )

    return conteudo


def inicializa_coluna(
    titulo: str,
    periodo: str,
    id_periodo: str,
    div_cartao_num_produtos: html.Div,
    div_cartao_num_marcas: html.Div,
    div_cartao_media_precos: html.Div,
    div_cartao_num_produtos_promocoes: html.Div,
    div_cartao_num_marcas_promocoes: html.Div,
    div_cartao_percentual_medio_desconto: html.Div,
    div_cartao_num_produtos_abaixo_200_reais: html.Div,
    div_cartao_produtos_com_mais_20_avaliacoes: html.Div,
    div_cartao_produtos_sem_avaliacao: html.Div,
    div_cartao_produtos_com_nota_maior_que_4: html.Div,
) -> html.Div:
    conteudo = html.Div(
        [
            html.H4(titulo, className="titulo_coluna"),
            html.Br(),
            html.Div(periodo, className="periodo_coluna", id=id_periodo),
            html.Br(),
            informacoes_coluna(
                div_cartao_num_produtos=div_cartao_num_produtos,
                div_cartao_num_marcas=div_cartao_num_marcas,
                div_cartao_media_precos=div_cartao_media_precos,
                div_cartao_num_produtos_promocoes=div_cartao_num_produtos_promocoes,
                div_cartao_num_marcas_promocoes=div_cartao_num_marcas_promocoes,
                div_cartao_percentual_medio_desconto=div_cartao_percentual_medio_desconto,
                div_cartao_num_produtos_abaixo_200_reais=div_cartao_num_produtos_abaixo_200_reais,
                div_cartao_produtos_com_mais_20_avaliacoes=div_cartao_produtos_com_mais_20_avaliacoes,
                div_cartao_produtos_sem_avaliacao=div_cartao_produtos_sem_avaliacao,
                div_cartao_produtos_com_nota_maior_que_4=div_cartao_produtos_com_nota_maior_que_4,
            ),
        ],
    )

    return conteudo


def inicializa_coluna_hoje(
    conexao: DuckDBPyConnection, data_coleta_mais_recente: str
) -> html.Div:
    data_coleta_formatada = formatar_data_pt_br(data_coleta_mais_recente)

    periodo = f"{data_coleta_formatada} - {data_coleta_formatada}"

    div_cartao_num_produtos = cartao_num_produtos(
        valor=numero_produtos_hoje(conexao), sufixo="hoje"
    )

    div_cartao_num_marcas = cartao_num_marcas(
        valor=numero_marcas_hoje(conexao), sufixo="hoje"
    )

    div_cartao_media_precos = cartao_media_precos(
        valor=media_precos_hoje(conexao), sufixo="hoje"
    )

    div_cartao_num_produtos_promocoes = cartao_num_produtos_promocoes(
        valor=numero_produtos_em_promocao_hoje(conexao), sufixo="hoje"
    )

    div_cartao_num_marcas_promocoes = cartao_num_marcas_promocoes(
        valor=numero_marcas_em_promocao_hoje(conexao), sufixo="hoje"
    )

    div_cartao_percentual_medio_desconto = cartao_percentual_medio_desconto(
        valor=percentual_medio_desconto_hoje(conexao), sufixo="hoje"
    )

    div_cartao_num_produtos_abaixo_200_reais = (
        cartao_produtos_abaixo_de_200_reais(
            valor=numero_produtos_abaixo_de_200_reais_hoje(conexao),
            sufixo="hoje",
        )
    )

    div_cartao_produtos_com_mais_20_avaliacoes = (
        cartao_produtos_com_mais_20_avaliacoes(
            valor=numero_produtos_com_20_ou_mais_avaliacoes_hoje(conexao),
            sufixo="hoje",
        )
    )

    div_cartao_produtos_sem_avaliacao = cartao_produtos_sem_avaliacao(
        valor=numero_produtos_sem_avaliacoes_hoje(conexao), sufixo="hoje"
    )

    div_cartao_produtos_com_nota_maior_que_4 = (
        cartao_produtos_com_nota_maior_que_4(
            valor=numero_produtos_com_nota_superior_4_hoje(conexao),
            sufixo="hoje",
        )
    )

    return inicializa_coluna(
        titulo="Hoje",
        periodo=periodo,
        id_periodo="pagina_1_periodo_hoje",
        div_cartao_num_produtos=div_cartao_num_produtos,
        div_cartao_num_marcas=div_cartao_num_marcas,
        div_cartao_media_precos=div_cartao_media_precos,
        div_cartao_num_produtos_promocoes=div_cartao_num_produtos_promocoes,
        div_cartao_num_marcas_promocoes=div_cartao_num_marcas_promocoes,
        div_cartao_percentual_medio_desconto=div_cartao_percentual_medio_desconto,
        div_cartao_num_produtos_abaixo_200_reais=div_cartao_num_produtos_abaixo_200_reais,
        div_cartao_produtos_com_mais_20_avaliacoes=div_cartao_produtos_com_mais_20_avaliacoes,
        div_cartao_produtos_sem_avaliacao=div_cartao_produtos_sem_avaliacao,
        div_cartao_produtos_com_nota_maior_que_4=div_cartao_produtos_com_nota_maior_que_4,
    )


def inicializa_coluna_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
    sufixo: str,
) -> html.Div:
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    periodo = f"{data_inicio_formatada} - {data_fim_formatada}"

    titulo = ""

    if sufixo == "escolhido":
        titulo = "Período Escolhido"
    else:
        titulo = "Período Histórico"

    div_cartao_num_produtos = cartao_num_produtos(
        valor=media_produtos_periodo(conexao, data_inicio, data_fim),
        sufixo=sufixo,
    )

    div_cartao_num_marcas = cartao_num_marcas(
        valor=media_marcas_periodo(conexao, data_inicio, data_fim),
        sufixo=sufixo,
    )

    div_cartao_media_precos = cartao_media_precos(
        valor=media_precos_periodo(conexao, data_inicio, data_fim),
        sufixo=sufixo,
    )

    div_cartao_num_produtos_promocoes = cartao_num_produtos_promocoes(
        valor=media_produtos_em_promocao_periodo(
            conexao, data_inicio, data_fim
        ),
        sufixo=sufixo,
    )

    div_cartao_num_marcas_promocoes = cartao_num_marcas_promocoes(
        valor=media_marcas_em_promocao_periodo(conexao, data_inicio, data_fim),
        sufixo=sufixo,
    )

    div_cartao_percentual_medio_desconto = cartao_percentual_medio_desconto(
        valor=media_percentual_desconto_periodo(conexao, data_inicio, data_fim),
        sufixo=sufixo,
    )

    div_cartao_num_produtos_abaixo_200_reais = (
        cartao_produtos_abaixo_de_200_reais(
            valor=media_produtos_abaixo_de_200_reais_periodo(
                conexao, data_inicio, data_fim
            ),
            sufixo=sufixo,
        )
    )

    div_cartao_produtos_com_mais_20_avaliacoes = (
        cartao_produtos_com_mais_20_avaliacoes(
            valor=media_produtos_com_20_ou_mais_avaliacoes_periodo(
                conexao, data_inicio, data_fim
            ),
            sufixo=sufixo,
        )
    )

    div_cartao_produtos_sem_avaliacao = cartao_produtos_sem_avaliacao(
        valor=media_produtos_sem_avaliacoes_periodo(
            conexao, data_inicio, data_fim
        ),
        sufixo=sufixo,
    )

    div_cartao_produtos_com_nota_maior_que_4 = (
        cartao_produtos_com_nota_maior_que_4(
            valor=media_produtos_com_nota_superior_4_periodo(
                conexao, data_inicio, data_fim
            ),
            sufixo=sufixo,
        )
    )

    return inicializa_coluna(
        titulo=titulo,
        periodo=periodo,
        id_periodo=f"pagina_1_periodo_{sufixo}",
        div_cartao_num_produtos=div_cartao_num_produtos,
        div_cartao_num_marcas=div_cartao_num_marcas,
        div_cartao_media_precos=div_cartao_media_precos,
        div_cartao_num_produtos_promocoes=div_cartao_num_produtos_promocoes,
        div_cartao_num_marcas_promocoes=div_cartao_num_marcas_promocoes,
        div_cartao_percentual_medio_desconto=div_cartao_percentual_medio_desconto,
        div_cartao_num_produtos_abaixo_200_reais=div_cartao_num_produtos_abaixo_200_reais,
        div_cartao_produtos_com_mais_20_avaliacoes=div_cartao_produtos_com_mais_20_avaliacoes,
        div_cartao_produtos_sem_avaliacao=div_cartao_produtos_sem_avaliacao,
        div_cartao_produtos_com_nota_maior_que_4=div_cartao_produtos_com_nota_maior_que_4,
    )


def atualiza_coluna_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
) -> list[str]:
    media_produtos = media_produtos_periodo(conexao, data_inicio, data_fim)

    media_marcas = media_marcas_periodo(conexao, data_inicio, data_fim)

    media_precos = media_precos_periodo(conexao, data_inicio, data_fim)

    media_produtos_em_promocao = media_produtos_em_promocao_periodo(
        conexao, data_inicio, data_fim
    )

    media_marcas_em_promocao = media_marcas_em_promocao_periodo(
        conexao, data_inicio, data_fim
    )

    media_percentual_desconto = media_percentual_desconto_periodo(
        conexao, data_inicio, data_fim
    )

    media_produtos_abaixo_de_200_reais = (
        media_produtos_abaixo_de_200_reais_periodo(
            conexao, data_inicio, data_fim
        )
    )

    media_produtos_com_nota_superior_4 = (
        media_produtos_com_nota_superior_4_periodo(
            conexao, data_inicio, data_fim
        )
    )

    media_produtos_com_20_ou_mais_avaliacoes = (
        media_produtos_com_20_ou_mais_avaliacoes_periodo(
            conexao, data_inicio, data_fim
        )
    )

    media_produtos_sem_avaliacoes = media_produtos_sem_avaliacoes_periodo(
        conexao, data_inicio, data_fim
    )

    return [
        media_produtos,
        media_marcas,
        media_precos,
        media_produtos_em_promocao,
        media_marcas_em_promocao,
        media_percentual_desconto,
        media_produtos_abaixo_de_200_reais,
        media_produtos_com_nota_superior_4,
        media_produtos_com_20_ou_mais_avaliacoes,
        media_produtos_sem_avaliacoes,
    ]
