import dash_bootstrap_components as dbc
import plotly.express as px
import polars as pl
from dash import Dash, Input, Output, callback, dash_table, dcc, html
from modulos.uteis import ler_sql

df = pl.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

df_2 = ler_sql.ler_query("../sql/queries/data_coleta_dados.sql")

df_3 = ler_sql.ler_query("../sql/queries/marcas_mais_encontradas.sql")


def cabecalho():
    titulo_1 = html.Div(
        children="Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        className="text-primary text-center fs-3",
    )

    data_coleta = df_2.item(0, 0)

    data_coleta_html = html.Div(
        children=f"Data Coleta: {data_coleta}",
        className="text-center",
    )

    linha = dbc.Row([titulo_1, data_coleta_html])

    return linha


def kpi_principais_sistema():
    subtitulo = html.H3(
        children="KPIs principais do sistema", style={"textAlign": "center"}
    )

    label_1 = html.P(
        children="Número Total de Itens", style={"textAlign": "center"}
    )

    label_2 = html.P(
        children="Número de Marcas Únicas", style={"textAlign": "center"}
    )

    label_3 = html.P(
        children="Preço Médio Atual (R$)", style={"textAlign": "center"}
    )

    quebra_linha = html.Hr()

    lista = [subtitulo, label_1, label_2, label_3, quebra_linha]

    return lista


def top_10_marcas_mais_encontradas():
    titulo = html.H3(
        children="Top 10 marcas mais encontradas",
        style={"textAlign": "center"},
    )

    tabela = dash_table.DataTable(data=df.to_dict(as_series=False), page_size=5)

    grafico = dcc.Graph(
        figure=px.bar(df, x="Marca", y="Qtd Produtos"), id="graph-content"
    )

    quebra_linha = html.Hr()

    lista = [titulo, tabela, grafico, quebra_linha]

    return lista


def preco_medio_por_marca():
    titulo = html.H3(
        children="Preço médio por marca",
        style={"textAlign": "center"},
    )

    quebra_linha = html.Hr()

    lista = [titulo, quebra_linha]

    return lista


def satisfacao_media_por_marca():
    titulo = html.H3(
        children="Satisfação Média por marca",
        style={"textAlign": "center"},
    )

    lista = [titulo]

    return lista


def testando_coisas():
    titulo = html.H3(
        children="Aprendendo",
        className="text-center fs-3",
    )

    opcoes = dbc.RadioItems(
        options=[
            {"label": x, "value": x} for x in ["pop", "lifeExp", "gdpPercap"]
        ],
        value="lifeExp",
        inline=True,
        id="radio-buttons-final",
    )

    tabela = dash_table.DataTable(
        data=df_3.to_dicts(),
        page_size=12,
        style_table={"overflowX": "auto"},
    )

    grafico = dcc.Graph(figure={}, id="my-first-graph-final")

    coluna_1 = dbc.Col([tabela], width=6)

    coluna_2 = dbc.Col([grafico], width=6)

    linha_1 = dbc.Row([titulo])

    linha_2 = dbc.Row([opcoes])

    linha_3 = dbc.Row([coluna_1, coluna_2])

    container = dbc.Container([linha_1, linha_2, linha_3])

    return container


# Add controls to build the interaction
@callback(
    Output(component_id="my-first-graph-final", component_property="figure"),
    Input(component_id="radio-buttons-final", component_property="value"),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    return fig


def dashboard():
    external_stylesheets = [dbc.themes.CERULEAN]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = dbc.Container(
        [
            cabecalho(),
            testando_coisas(),
        ],
        fluid=True,
    )

    app.run(debug=True)
