import dash_bootstrap_components as dbc
import plotly.express as px
import polars as pl
from dash import Dash, Input, Output, callback, dash_table, dcc, html
from dashboard import (
    minha_sidebar,
    pagina_1,
    pagina_2,
    pagina_404,
    pagina_home,
    titulos,
)
from modulos.uteis import ler_sql


def conteudo_pagina_atual() -> html.Div:
    content_style = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    conteudo = html.Div(id="page-content", style=content_style)

    linha = dbc.Row([conteudo])

    return linha


def cabecalho(df: pl.DataFrame):
    titulo_1 = html.Div(
        children="Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        className="text-primary text-center fs-3",
    )

    caminho_query = "../sql/queries/data_coleta_dados.sql"

    df_data_coleta = ler_sql.query_df(caminho_query, df)

    data_coleta = df_data_coleta.item(0, 0)

    horario_coleta = df_data_coleta.item(0, 1)

    data_coleta_html = html.Div(
        children=f"Data Coleta: {data_coleta} - {horario_coleta}",
        className="text-center",
    )

    linha = dbc.Row([titulo_1, data_coleta_html])

    return linha


def testando_coisas(df: pl.DataFrame):
    df_filtrado = df.select(
        pl.col("marca"),
        pl.col("preco_atual"),
        pl.col("preco_velho"),
    ).filter(pl.col("marca").is_in(["OLYMPIKUS", "MIZUNO", "ADIDAS", "FILA"]))

    titulo = html.H3(
        children="Aprendendo",
        className="text-center fs-3",
    )

    opcoes = dbc.RadioItems(
        options=[
            {"label": x, "value": x} for x in ["preco_atual", "preco_velho"]
        ],
        value="preco_atual",
        inline=True,
        id="radio-buttons-final",
    )

    tabela = dash_table.DataTable(
        data=df_filtrado.to_dicts(),
        page_size=12,
        style_table={"overflowX": "auto"},
        id="minha_tabela",
    )

    grafico = dcc.Graph(figure={}, id="my-first-graph-final")

    coluna_1 = dbc.Col([tabela], width=6)

    coluna_2 = dbc.Col([grafico], width=6)

    linha_0 = dbc.Row([html.Hr()])

    linha_1 = dbc.Row([titulo])

    linha_2 = dbc.Row([opcoes])

    linha_3 = dbc.Row([coluna_1, coluna_2])

    container = dbc.Container([linha_0, linha_1, linha_2, linha_3])

    return container


# Add controls to build the interaction
# @callback(
#    Output(component_id="my-first-graph-final", component_property="figure"),
#    Input(component_id="radio-buttons-final", component_property="value"),
#    Input(component_id="minha_tabela", component_property="data"),
# )
def update_graph(col_chosen, df_dicts):
    df = pl.DataFrame(df_dicts)

    fig = px.histogram(df, x="marca", y=col_chosen, histfunc="avg")
    return fig


@callback(
    Output(component_id="page-content", component_property="children"),
    Input(component_id="url", component_property="pathname"),
)
def render_page_content(pathname):
    if pathname == "/":
        return pagina_home.home()
    elif pathname == "/page-1":
        return pagina_1.pagina_1()
    elif pathname == "/page-2":
        return pagina_2.pagina_2()
    # If the user tries to reach a different page, return a 404 message
    return pagina_404.pagina_404(pathname)


def meu_dashboard():
    # caminho_query = "../sql/queries/dados_mais_recentes.sql"

    # df = ler_sql.query_banco_de_dados_apenas_leitura(caminho_query)

    external_stylesheets = [dbc.themes.LUMEN]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = dbc.Container(
        [
            dcc.Location(id="url"),
            minha_sidebar.sidebar(),
            # cabecalho(df),
            conteudo_pagina_atual(),
            # testando_coisas(df),
        ],
        fluid=True,
    )

    app.run(debug=True)
